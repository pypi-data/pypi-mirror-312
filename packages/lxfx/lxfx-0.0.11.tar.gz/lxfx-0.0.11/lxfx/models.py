import torch
import torch.nn as nn

import logging

from lxfx.utils import createLogger

class FCBlock(nn.Module): # ForecastBlock
    def __init__(self, in_features, hidden_size, out_size, nature = "lstm", dropout= 0.2,
                 num_layers = 1, bidirectional = False, activation = "tanh",
                 use_batch_norm = False, pass_block_hidden_state = False):
        """
        Initializes the FCBlock with the provided parameters.

        Parameters:
            in_features (int): The number of input features.
            hidden_size (int): The size of the hidden layer.
            out_size (int): The size of the output layer.
            nature (str): The type of the block, one of "lstm", "rnn", "gru".
            dropout (float): The dropout rate.
            num_layers (int): The number of layers.
            bidirectional (bool): Whether the block is bidirectional.
            activation (str): The activation function, one of "tanh", "relu".
            use_batch_norm (bool): Whether to use batch normalization.
            pass_block_hidden_state: Whether to pass the hidden state of the first lstm to the next
        """
        super(FCBlock, self).__init__()
        self.nature = nature
        self.activation = activation
        if self.activation == "tanh":
            self.activation_function = nn.Tanh()
        elif self.activation == "relu":
            self.activation_function = nn.ReLU()
        self.num_layers = num_layers
        self.in_features = in_features
        self.hidden_size1 = hidden_size 
        self.output_size = out_size
        self.bidirectional = bidirectional
        self.pass_block_hidden_state = pass_block_hidden_state
        self.use_batch_norm = use_batch_norm
        self.dropout = dropout if self.num_layers > 1 else 0
        self.hidden_size2 = self.hidden_size1*2 if self.bidirectional is True else self.hidden_size1
        if self.nature == "lstm":
            self.l1 = nn.LSTM(self.in_features,hidden_size=self.hidden_size1, dropout=self.dropout,  num_layers=self.num_layers, bidirectional=self.bidirectional, batch_first=True)
            self.l2 = nn.LSTM(self.hidden_size2,hidden_size=self.output_size, dropout=self.dropout,  num_layers=self.num_layers, bidirectional=self.bidirectional, batch_first=True)
        elif self.nature == "rnn":
            self.l1 = nn.RNN(self.in_features,hidden_size=self.hidden_size1, dropout=self.dropout,  num_layers=self.num_layers, bidirectional=self.bidirectional, batch_first=True)
            self.l2 = nn.RNN(self.hidden_size2,hidden_size=self.output_size, dropout=self.dropout,  num_layers=self.num_layers, bidirectional=self.bidirectional, batch_first=True)            
        elif self.nature == "gru":
            self.l1 = nn.GRU(self.in_features,hidden_size=self.hidden_size1, dropout=self.dropout,  num_layers=self.num_layers, bidirectional=self.bidirectional, batch_first=True)
            self.l2 = nn.GRU(self.hidden_size2,hidden_size=self.output_size, dropout=self.dropout,  num_layers=self.num_layers, bidirectional=self.bidirectional, batch_first=True)

        # Add BatchNorm1d layers if use_batch_norm is True
        if self.use_batch_norm:
            bn_hidden_size2 = self.output_size*2 if self.bidirectional else self.output_size
            self.batch_norm1 = nn.BatchNorm1d(self.hidden_size2)
            self.batch_norm2 = nn.BatchNorm1d(bn_hidden_size2)

    def forward(self,x, prev_states = None):
        if self.nature == "lstm":
            output, (h1, c1) = self.l1(x, prev_states)
        else:
            output, h1 = self.l1(x, prev_states)

        # Apply BatchNorm1d if enabled
        # Note: batch_norm expects the input shape of (batch_size ,num_features, seq_length)
        # yet LSTMS, GRUS, RNNS, output shape is ( batch_size, seq_length, num_features) when batch_first is True
        if self.use_batch_norm:
            output = self.batch_norm1(output.transpose(1, 2)).transpose(1, 2)

        output = self.activation_function(output)

        # Pass to the next layer
        if self.nature == "lstm":
            if self.pass_block_hidden_state:
                output, (h2, c2) = self.l2(output, (h1, c1))
            else:
                output, (h2, c2) = self.l2(output)
            if self.use_batch_norm:
                output = self.batch_norm2(output.transpose(1, 2)).transpose(1, 2)
            return output, (h2, c2)
        else:
            if self.pass_block_hidden_state:
                output, h2 = self.l2(output, h1)
            else:
                output, h2 = self.l2(output)
            if self.use_batch_norm:
                output = self.batch_norm2(output.transpose(1, 2)).transpose(1, 2)
            return output, h2
        
class FxFCModel(nn.Module): # fxForeCastModel
    def __init__(self, num_features,
                 block_type = "lstm",
                 out_features = 1,
                 units:list = None,
                 num_layers = 1,
                 is_encoder = False,
                 encoder_latent_dim = None,
                 is_decoder = False, 
                 out_units:list = None,
                 activation:str = "tanh",
                 bidirectional = False, 
                 pass_states = False,
                 use_batch_norm = False, 
                 pass_block_hidden_state = False, 
                 decoder_out_features = None,
                 dropout = 0.2, 
                 ):
        """
        Parameters:
            num_features: the number of features per sequence eg if we have a seq [1., 2., 3., 4.] then the n_features = 4
            block_type: This is one of "lstm", "rnn", "gru" for the FCBlocks
            out_features: the number of features that we are trying to predict forexample if we trying to predict the close and moving average then this = 2
            units: A list of hidden sizes as they are supposed to propagate through the blocks
            is_encoder: Whether the model is to be used as an encoder in an autoencoder architecture
            encoder_latent_dim: the dimension for the latent representation of the encoder
            is_decoder: Whether the model is to be used as a decoder in an autoencoder Architecture
            out_units (list): The output sizes of the the blocks. This also affects the input shapes of the block of the preceeding blocks after the first has been set
            activation: The activation to use. One of "tanh", "relu"
            bidirectional: Whether the FCBlocks are bidirectional
            pass_states: Whether to pass the states to the next layer
            use_batch_norm: Whether to use batch normalization in the FCBlocks
            pass_block_hidden_state: Whether to pass the hidden state of the first lstm in the fcblock to the next
            decorder_out_features: if the model is to be used as a decoder then this is the actual number of features that we are trying to predict forexample if we trying to predict the close and moving average then this = 2
            dropout: The dropout rate
        todo:
            Initialize a list of bidirectional states and num_layers states for the FCBlocks(this requires not only saving 
            the model state dict but in order to reconstruct the model you must have saved these states in an extenal file)
        """
        super(FxFCModel, self).__init__() 

        self.model_type = "FxFCModel"

        self.num_features = num_features
        self.blocks = nn.ModuleList()
        self.block_type = block_type
        self.units = units
        self.out_units = out_units
        self.bidirectional = bidirectional
        self.num_layers = num_layers
        self.is_encoder = is_encoder
        self.use_batch_norm = use_batch_norm
        self.encoder_latent_dim = encoder_latent_dim
        self.decoder_out_features = decoder_out_features
        self.is_decoder = is_decoder
        self.activation = activation
        self.pass_states = pass_states
        self.dropout = dropout
        self.pass_block_hidden_state = pass_block_hidden_state
        self.console_logger = createLogger(logging.INFO, is_consoleLogger=True)

        if self.out_units:    
            if len(self.out_units) > 1 and not all(x == self.out_units[0] for x in self.out_units):
                self.pass_states = False
            self.pass_block_hidden_state = False

        # if self.out_units and len(self.out_units) == len(self.units):
        for i in range(len(self.units)):
            if i == 0:
                in_features = self.num_features   
            else:
                if not self.out_units:
                    in_features = self.units[i-1] if not self.bidirectional else self.units[i-1]*2
                else:
                    in_features = self.out_units[i-1] if not self.bidirectional else self.out_units[i-1]*2
            hidden_size = self.units[i]
            output_size = self.out_units[i] if self.out_units else hidden_size
            self.blocks.append(FCBlock(in_features,
                                       hidden_size,
                                       output_size,
                                       self.block_type,
                                       dropout=self.dropout,
                                       num_layers=self.num_layers,
                                       bidirectional=self.bidirectional,
                                       activation=self.activation,
                                       use_batch_norm = self.use_batch_norm,
                                       pass_block_hidden_state = self.pass_block_hidden_state))
        self.out_features = out_features
        if self.bidirectional:
            if  not self.out_units:
                self.fc_in_features = self.units[-1]*2
            else:
                self.fc_in_features = self.out_units[-1]*2
        else:
            if  not self.out_units:
                self.fc_in_features = self.units[-1]
            else:
                self.fc_in_features = self.out_units[-1]

        if self.is_encoder:
            out_features = self.encoder_latent_dim
        elif self.is_decoder:
            out_features = self.decoder_out_features
        
        self.fc = nn.Linear(in_features = self.fc_in_features, out_features=out_features)

    def config_dict(self):
        return {
            "num_features": self.num_features,
            "block_type": self.block_type,
            "units": self.units,
            "out_units": self.out_units,
            "bidirectional": self.bidirectional,
            "num_layers": self.num_layers,
            "is_encoder": self.is_encoder,
            "use_batch_norm": self.use_batch_norm,
            "encoder_latent_dim": self.encoder_latent_dim,
            "decoder_out_features": self.decoder_out_features,
            "is_decoder": self.is_decoder,
            "activation": self.activation,
            "pass_states": self.pass_states,
            "pass_block_hidden_state": self.pass_block_hidden_state,
            "dropout": self.dropout
        }

    def forward(self, x, prev_state = None):
        for idx, block in enumerate(self.blocks):
            # note
            # lstm output: o, (h, c)
            # rnn and gru output: o, h
            if idx > 0 and self.pass_states:
                if self.block_type == "lstm":
                    x, (h2, c2) = block(x, prev_state)
                    prev_state = (h2, c2)
                else:
                    x, h2 = block(x, prev_state)
                    prev_state = h2
            else:
                if self.block_type == "lstm":
                    x, (h2, c2) = block(x) # the 2 represents that these states are for the second block in the FCBlock
                    prev_state = (h2, c2)
                else:
                    x, h2 = block(x)    
                    prev_state = h2

        if self.is_encoder or self.is_decoder:
            return x, prev_state
        else:
            # h2 = h2.squeeze(0) # this only works on single single direction layers
            final_output = x[:, -1, :]
            x = self.fc(final_output)
            return x
            
class ConcatenationAttention(nn.Module):
    """
    Implements an attention mechanism that computes a context vector by comparing
    the encoder's output with the decoder's hidden state.

    Attributes:
        encoder_output (torch.Tensor): The output from the encoder, with shape 
            (batch_size, seq_len, latent_dim).
        decoder_h_input (torch.Tensor): The hidden state from the decoder, with shape 
            (batch_size, hidden_size).
        encoder_latent_dim (int): The number of features in the encoder output, equivalent to latent_dim.
        encoder_seq_len (int): The sequence length of the encoder output.
        decoder_hidden_size (int): The number of features in the decoder's hidden state.
        softmax (nn.Softmax): Softmax layer to normalize alignment scores into probabilities.
        tanh (nn.Tanh): Tanh activation function applied to the energy scores.
        learnable_weight (nn.Parameter): A learnable parameter used to compute alignment scores.
        attn (nn.Linear): Linear layer that projects concatenated encoder and decoder features 
            into a space of size encoder_latent_dim.

    Methods:
        forward(encoder_input=None, decoder_h_input=None):
            Computes the context vector by aligning the encoder's output with the decoder's hidden state.
            The context vector is a weighted sum of the encoder_input based on alignment scores.

            Parameters:
                encoder_input (torch.Tensor, optional): The encoder output. Defaults to the initialized value.
                decoder_h_input (torch.Tensor, optional): The decoder hidden state. Defaults to the initialized value.

            Returns:
                torch.Tensor: The context vector with shape (batch_size, encoder_latent_dim).

    Detailed Process:
        1. Ensure encoder_input and decoder_h_input are not None. If they are, use the initialized values.
        2. Reshape decoder_h_input to (batch_size, 1, decoder_hidden_size) to facilitate broadcasting.
        3. Repeat decoder_h_input across the sequence length to match encoder_input's shape.
        4. Concatenate encoder_input and decoder_h_input along the feature dimension.
        5. Project the concatenated input into a space of size encoder_latent_dim using a linear layer, 
           followed by a tanh activation.
        6. Transpose the energy tensor to prepare for batch matrix multiplication.
        7. Repeat learnable_weight for each batch to match the batch size of energy.
        8. Compute alignment scores by performing a batch matrix multiplication between learnable_weight and energy.
        9. Normalize the alignment scores to probabilities using softmax.
        10. Compute the context vector as a weighted sum of the encoder outputs, using the alignment scores.
    """
    def __init__(self, hidden_size, decoder_hidden_size):
        """
        The hidden_size is the size of the output of the encoder whose shape is (batch_size, seq_len, encoder_latent_dim)
        The decoder_h_input is the hidden state of the decoder whose shape is (batch_size, hidden_size)
        Parameters:
            hidden_size: The encoder latent dim
            decoder_h_input_size: The hidden state size of the decoder
        """
        super(ConcatenationAttention, self).__init__()

        self.encoder_latent_dim = hidden_size
        self.decoder_hidden_size = decoder_hidden_size

        self.learnable_weight = nn.Parameter(torch.randn(1, self.encoder_latent_dim))
        self.attn = nn.Linear(self.encoder_latent_dim + self.decoder_hidden_size, self.encoder_latent_dim)

        self.softmax = nn.Softmax(dim=1)
        self.tanh = nn.Tanh()

    def forward(self, encoder_input:torch.Tensor = None, decoder_h_input:torch.Tensor = None):
        """
        Parameters:
            encoder_input(torch.Tensor): Input token which is by default the last timestep hidden encoder state of size (batch_size, seq_len, encoder_latent_dim)
            decoder_h_input(torch.Tensor): Decoder hidden state of size (batch_size, decoder_hidden_size)
        """
        # encoder_input size = (batch_size, seq_len, encoder_latent_dim)
        # decoder_h_input size = (batch_size, decoder_hidden_size)

        decoder_h_input = decoder_h_input.unsqueeze(1) # size = (batch_size, 1, decoder_hidden_size)
        
        # Repeat the decoder_h_input to match the sequence length of the encoder_input
        decoder_h_input = decoder_h_input.repeat(1, encoder_input.size(1), 1) # size = (batch_size, seq_len, encoder_latent_dim)
        
        # Concatenate the encoder_input and decoder_h_input along the feature dimension
        concat_input = torch.cat((encoder_input, decoder_h_input), dim=2)
        
        # Pass the concatenated input through a linear layer
        energy = self.tanh(self.attn(concat_input)) # size = (batch_size, seq_len, encoder_latent_dim)
        
        # compute allignment scores
        energy = energy.permute(0, 2, 1) # size = (batch_size, encoder_latent_dim, seq_len)
        
        # repeat the learnable weight for each batch
        learnable_weight = self.learnable_weight.repeat(energy.size(0), 1).unsqueeze(1) # size = (batch_size, 1, encoder_latent_dim)
        
        # Multipy the learnable weight vector with each sequence in the energy tensor for each batch
        allignment_score = torch.bmm(learnable_weight, energy).squeeze(1) # size = (batch_size, seq_len)
        
        # compute attention weights
        attention_weights = self.softmax(allignment_score) # size = (batch_size, seq_len)

        # compute the context vector as a weighted sum of the encoder_input
        # Multiply each encoder input with the allignment score and sum up the result
        context_vector = torch.bmm(attention_weights.unsqueeze(1), encoder_input).squeeze(1) # size = (batch_size, encoder_latent_dim)

        """Summary:
        The context vector is a weighted sum of the encoder_input based on the allignment scores.
        The allignment scores are the result of comparing the encoder_input and the decoder_h_input

        The result here is now going to be concatenated with the decorder input before being passed to the lstm of the decoder
        """

        return context_vector, attention_weights 

class FxFCEncoder(nn.Module):
    def __init__(self, num_features,
                 block_type="lstm",
                 units=None,
                 out_units=None,
                 num_layers=1, 
                 activation="tanh",
                 latent_dim=None, 
                 dropout=0.2,
                 use_batch_norm=False,
                 bidirectional=False,
                 pass_states = False,
                 pass_block_hidden_state=False,
                 is_attentive=False):
        """
        Parameters:
            num_features: the number of features per sequence
            block_type: This is one of "lstm", "rnn", "gru" for the FCBlocks
            units: A list of hidden sizes as they are supposed to propagate through the blocks
            out_units: The output sizes of the blocks. This also affects the input shapes of the block of the preceding blocks after the first has been set
            num_layers: The number of layers in the FCBlocks
            activation: The activation to use. One of "tanh", "relu"
            latent_dim: the dimension for the latent representation of the encoder
            dropout: The dropout rate
            use_batch_norm: Whether to use batch normalization in the FCBlocks
            bidirectional: Whether the FCBlocks are bidirectional
            pass_states: Whether to pass hidden states among the FCBlocks
            pass_block_hidden_state: Whether to pass the hidden state of the first lstm in the fcblock to the next
            is_attentive: Whether to make the encoder attentive by activating attention
        """
        super(FxFCEncoder, self).__init__()

        self.model_type = "FxFCEncoder"

        self.num_features = num_features 
        self.block_type = block_type 
        self.units = units 
        self.bidirectional = bidirectional
        self.out_units = out_units
        self.num_layers = num_layers 
        self.activation = activation
        self.latent_dim = latent_dim
        self.use_batch_norm = use_batch_norm
        self.dropout = dropout
        self.pass_states = pass_states
        self.pass_block_hidden_state = pass_block_hidden_state
        self.is_attentive = is_attentive

        self.encoder = FxFCModel(num_features=self.num_features,
                                 block_type=self.block_type,
                                 units=self.units,
                                 out_units=self.out_units,
                                 num_layers=self.num_layers,
                                 is_encoder=True,
                                 activation=self.activation,
                                 encoder_latent_dim=self.latent_dim,
                                 dropout=self.dropout,
                                 bidirectional=self.bidirectional, 
                                 use_batch_norm=self.use_batch_norm,
                                 pass_states=self.pass_states,
                                 pass_block_hidden_state=self.pass_block_hidden_state,
                                 )
        
        if self.out_units is None:
            self.last_layer_feature_dim = self.units[-1] if self.bidirectional is False else self.units[-1]*2
        else:
            self.last_layer_feature_dim = self.out_units[-1] if self.bidirectional is False else self.out_units[-1]*2
            
        self.first_layer_feature_dim = self.units[0]

    def forward(self, input_data):
        # Initialize hidden and cell states
        h_t, c_t = (torch.zeros(self.num_layers, input_data.size(0), self.first_layer_feature_dim).to(input_data.device),
                    torch.zeros(self.num_layers, input_data.size(0), self.first_layer_feature_dim).to(input_data.device))
        
        # Initialize the encoded output
        input_encoded = torch.zeros(input_data.size(0), input_data.size(1), self.last_layer_feature_dim).to(input_data.device)
        
        # Process each timestep in the sequence
        for t in range(input_data.size(1)):
            x_t = input_data[:, t, :].unsqueeze(1)  # Get the t-th timestep
            if self.block_type == "lstm":
                out_, (h_t, c_t) = self.encoder(x_t, (h_t, c_t))
            else:
                out_, h_t = self.encoder(x_t, h_t)

            if t <= input_data.size(1)-2: # save all but not the last
                if self.num_layers == 1 and self.bidirectional is False:
                    input_encoded[:, t, :] = h_t[0]  # Store the last layer's hidden state
                else:
                    # todo :("Bidirectional or num layers are not yet handled")
                    input_encoded[:, t, :] = out_[:, -1, :]
            else:
                last_hidden_size = h_t[0]

        if self.is_attentive:
            return self.encoder.fc(last_hidden_size), self.encoder.fc(input_encoded)
        else:
            return self.encoder.fc(last_hidden_size)

class FxFCDecoder(nn.Module):
    def __init__(self, latent_dim,
                 target_features=1,
                 block_type="lstm",
                 units=None,
                 out_units=None,
                 num_layers=1,
                 activation="tanh", 
                 dropout=0.2,
                 use_batch_norm=False,
                 pass_states = False, 
                 pass_block_hidden_state=False,
                 initialize_weights=False,
                 initializer_method=None,
                 future_pred_length=1, 
                 is_attentive = False):
        """
        Parameters:
            latent_dim: the number of features in the latent dim.
            target_features: the number of features that we are trying to predict
            block_type: This is one of "lstm", "rnn", "gru" for the FCBlocks
            units: A list of hidden sizes as they are supposed to propagate through the blocks
            out_units: The output sizes of the blocks. This also affects the input shapes of the block of the preceding blocks after the first has been set
            num_layers: The number of layers in the FCBlocks
            activation: The activation to use. One of "tanh", "relu"
            dropout: The dropout rate
            use_batch_norm: Whether to use batch normalization in the FCBlocks
            pass_states: Whether to pass hidden states among FCBlocks
            pass_block_hidden_state: Whether to pass the hidden state of the first lstm in the fcblock to the next
            initialize_weights: Whether to initialize the weights of the decoder
            initializer_method: The method to use to initialize the weights. One of "xavier", "uniform", "zeros"
            future_pred_length: The length of future predictions
            is_attentive: Whether or not to make the decoder attentive by activating attention
        """
        super(FxFCDecoder, self).__init__()

        self.console_logger = createLogger(log_level= logging.WARNING, is_consoleLogger=True)

        self.model_type = "FxFCDecoder"

        self.latent_dim = latent_dim
        self.block_type = block_type 
        self.units = units 
        self.out_units = out_units  
        self.num_layers = num_layers 
        self.activation = activation
        self.use_batch_norm = use_batch_norm
        self.target_features = target_features
        self.initialize_weights = initialize_weights
        self.initializer_method = initializer_method
        self.dropout = dropout
        self.pass_states = pass_states
        self.pass_block_hidden_state = pass_block_hidden_state
        self.future_pred_length = future_pred_length
        self.is_attentive = is_attentive

        self.decoder_hidden_size = self.units[-1] if not self.out_units else self.out_units[-1]
        
        if self.is_attentive:
            self.attention = ConcatenationAttention(self.latent_dim, self.latent_dim)
        
        self.decoder_in_features = 2*self.latent_dim if self.is_attentive else self.latent_dim

        self.decoder = FxFCModel(num_features=self.decoder_in_features,
                                 block_type=self.block_type, 
                                 units=self.units, 
                                 num_layers=self.num_layers, 
                                 is_decoder=True, 
                                 out_units=self.out_units, 
                                 activation=self.activation,
                                 dropout=self.dropout, 
                                 bidirectional=False, # this is a decoder no bidirectional
                                 use_batch_norm=self.use_batch_norm, 
                                 decoder_out_features=self.target_features,
                                 pass_states=self.pass_states,
                                 pass_block_hidden_state=self.pass_block_hidden_state)
        self.latent_dim_mapper = nn.Linear(self.decoder_hidden_size, self.latent_dim)
        self.tensor_initializer = TensorInitializer(method="xavier", num_layers=self.num_layers)

    def forward(self, last_encoder_hidden_state, encoder_outputs = None):
        """
        Parameters:
            last_encoder_hidden_state: The last hidden state of the decoder which is the first to be used by decoder 
        on the start of the generation. size: (batch_size, latent_dim)
            encoder_outputs: The other hidden states generating during the encoding phase. These are generally to be used 
        during the attention mechanism. size :(batch_size, seq_len, latent_dim)
        """
        outputs = []
        decoder_input = last_encoder_hidden_state
        prev_state = None
        if self.initialize_weights:
            if self.initializer_method == "xavier":
                h_t, c_t = (self.tensor_initializer.initializeTensor(),
                            self.tensor_initializer.initializeTensor())
                prev_state = (h_t, c_t)
            elif self.initializer_method == "zeros":
                h_t, c_t = (torch.zeros(self.num_layers, decoder_input.size(0), self.units[-1]).to(decoder_input.device),
                            torch.zeros(self.num_layers, decoder_input.size(0), self.units[-1]).to(decoder_input.device))
                prev_state = (h_t, c_t)
            else:
                prev_state = None
        else:
            prev_state = None

        # The encoder returns a tensor of size (batch_size, latent_dim)
        # Note: self.decoder expects a tensor of size (batch_size, seq_len, latent_dim)
        # Add a sequence length dimension to the encoded_input
        if not self.is_attentive:
            decoder_input = decoder_input.unsqueeze(1)
        else:
            # Apply attention to the decoder input
            # context_vector shape: (batch_size latent_dim)
            context_vector, attention_weights = self.attention(encoder_outputs, decoder_input)

            # Concatenate the context vector with the decoder input
            decoder_input = torch.cat((decoder_input.unsqueeze(1), context_vector.unsqueeze(1)), dim=2)
            # size = (batch_size, 1, encoder_latent_dim+decoder_input.shape[-1])

        prev_hidden_state = None
        for t in range(self.future_pred_length):
            if self.block_type == "lstm":
                if prev_state is not None:
                    output, (h_t, c_t) = self.decoder(decoder_input, prev_state)
                else:
                    output, (h_t, c_t) = self.decoder(decoder_input)
            else:
                if prev_state is not None:
                    output, h_t = self.decoder(decoder_input, prev_state)
                else:
                    output, h_t = self.decoder(decoder_input)

            mapped_decoder_output = self.latent_dim_mapper(output) # map the decoder hidden state to the latent dim
            mapped_hidden_state = mapped_decoder_output[:, -1, :] # same as h_t when no bidirectional and num_layers is 1 size = (batch_size, latent_dim)
            if self.is_attentive:
                # Apply attention
                if t > 0: # add previous hidden state to the encoder outputs to add value to context
                    encoder_outputs = torch.cat((encoder_outputs, prev_hidden_state.permute(1,0,2)), dim=1)

                context_vector, attention_weights = self.attention.forward(encoder_outputs, mapped_hidden_state)
                decoder_input = torch.cat((mapped_hidden_state.unsqueeze(1), context_vector.unsqueeze(1)), dim=2)

                prev_hidden_state = mapped_hidden_state.unsqueeze(0) # size = (1, batch_size, latent_dim) which is in the same format as the encoder_outputs ie (batch_size, seq_len, latent_dim)
            else:
                decoder_input = mapped_hidden_state.unsqueeze(1)
            
            pred = self.decoder.fc(output[:, -1, :])
            pred = pred.unsqueeze(0)
            outputs.append(pred)

        outputs = torch.cat(outputs, dim=0) # size = (future_pred_length, batch_size, target_features)
        outputs_shape = outputs.shape
        future_dim, batch_dim, features_dim = outputs_shape[0], outputs_shape[1], outputs_shape[2]
        outputs = outputs.view((batch_dim, future_dim, features_dim)) # size = (batch_size, future_pred_length, target_features)
        return outputs

class FxFCAutoEncoder(nn.Module):
    def __init__(self, num_features,
                 target_features=1,
                 future_pred_length=1,
                 block_types=("lstm", "lstm"),
                 units=None,
                 out_units=None,
                 num_layers=(1, 1),
                 activations=("tanh", "tanh"),
                 latent_dim=32,
                 dropout=(0.2, 0.2),
                 bidirectional=(False, False),
                 use_batch_norm=(False, False),
                 pass_states = (False, False),
                 pass_block_hidden_state=(False, False),
                 is_attentive=False):
        """
        Parameters:
            num_features: the number of features per sequence
            target_features: the number of features to predict
            future_pred_length: the length of future predictions
            block_types: A tuple of the block types for the encoder and decoder
            units: A tuple of the hidden sizes for the encoder and decoder
            out_units: A tuple of the output sizes for the encoder and decoder
            num_layers: A tuple of the number of layers for the encoder and decoder
            activations: A tuple of the activation functions for the encoder and decoder
            latent_dim: the dimension for the latent representation of the encoder
            dropout: A tuple of dropout rates for the encoder and decoder
            bidirectional: A tuple indicating if the encoder and decoder are bidirectional
            use_batch_norm: A tuple indicating if batch normalization is used in the encoder and decoder
            pass_block_hidden_state: A tuple indicating if the hidden state is passed in the encoder and decoder
            is_attentive: Whether to make the autoencoder attentive by activating attention
        """
        super(FxFCAutoEncoder, self).__init__()

        self.model_type = "FxFCAutoEncoder"

        self.num_features = num_features
        self.target_features = target_features
        self.future_pred_length = future_pred_length
        self.block_types = block_types
        self.is_attentive = is_attentive
        self.encoder_block_type = self.block_types[0]
        self.decoder_block_type = self.block_types[1]

        self.units = units
        self.encoder_units, self.decoder_units = self.units

        self.out_units = out_units
        if self.out_units:
            self.encoder_out_units = self.out_units[0]
            self.decoder_out_units = self.out_units[1]
        else:
            self.encoder_out_units = None
            self.decoder_out_units = None

        self.num_layers = num_layers
        self.encoder_num_layers = self.num_layers[0]
        self.decoder_num_layers = self.num_layers[1]

        self.activations = activations
        self.encoder_activation = self.activations[0]
        self.decoder_activation = self.activations[1]

        self.encoder_latent_dim = latent_dim

        self.dropout = dropout
        self.encoder_dropout = self.dropout[0]
        self.decoder_dropout = self.dropout[1]

        self.bidirectional = bidirectional
        self.encoder_bidirectional = self.bidirectional[0]

        self.use_batch_norm = use_batch_norm
        self.encoder_use_batch_norm = self.use_batch_norm[0]
        self.decoder_use_batch_norm = self.use_batch_norm[1]

        self.pass_states = pass_states
        self.encoder_pass_states = self.pass_states[0]
        self.decoder_pass_states = self.pass_states[1]

        self.pass_block_hidden_state = pass_block_hidden_state
        self.encoder_pass_block_hidden_state = self.pass_block_hidden_state[0]
        self.decoder_pass_block_hidden_state = self.pass_block_hidden_state[1]

        self.encoder = FxFCEncoder(num_features=self.num_features, 
                                   block_type=self.encoder_block_type,
                                   units=self.encoder_units, 
                                   out_units=self.encoder_out_units,
                                   num_layers=self.encoder_num_layers, 
                                   activation=self.encoder_activation,
                                   latent_dim=self.encoder_latent_dim, 
                                   dropout=self.encoder_dropout,
                                   bidirectional=self.encoder_bidirectional, 
                                   use_batch_norm=self.encoder_use_batch_norm,
                                   pass_block_hidden_state=self.encoder_pass_block_hidden_state,
                                   is_attentive=self.is_attentive,
                                   pass_states=self.encoder_pass_states)

        self.decoder = FxFCDecoder(latent_dim=self.encoder_latent_dim,
                                   block_type=self.decoder_block_type,
                                   units=self.decoder_units,
                                   out_units=self.decoder_out_units,
                                   num_layers=self.decoder_num_layers,
                                   activation=self.decoder_activation,
                                   target_features=self.target_features,
                                   dropout=self.decoder_dropout,
                                   use_batch_norm=self.decoder_use_batch_norm,
                                   pass_block_hidden_state=self.decoder_pass_block_hidden_state,
                                   future_pred_length=self.future_pred_length, 
                                   is_attentive=self.is_attentive,
                                   pass_states=self.decoder_pass_states)

    def config_dict(self):
        return {
            "num_features": self.num_features,
            "target_features": self.target_features,
            "future_pred_length": self.future_pred_length,
            "block_types": self.block_types,
            "units": self.units,
            "out_units": self.out_units,
            "num_layers": self.num_layers,
            "activations": self.activations,
            "latent_dim": self.encoder_latent_dim,
            "dropout": self.dropout,
            "bidirectional": self.bidirectional,
            "use_batch_norm": self.use_batch_norm,
            "pass_states":self.pass_states,  
            "pass_block_hidden_state": self.pass_block_hidden_state, 
            "is_attentive:" : self.is_attentive
        }

    def forward(self, input_seq):
        if self.is_attentive:
            encoded_vector, encoded_outputs = self.encoder(input_seq)  # size = (batch_size, latent_dim)
            preds = self.decoder.forward(encoded_vector, encoded_outputs)
        else:
            encoded_vector = self.encoder(input_seq)
            preds = self.decoder.forward(encoded_vector)
        return preds

class TensorInitializer:
    def __init__(self, method = None, x: torch.Tensor = None, num_layers = 1,
                 hidden_size = None):
        self.method = method
        self.tensor = x
        self.num_layers = num_layers
        self.hidden_size = hidden_size

    def initializeTensor(self):
        self.p_h = torch.zeros(self.num_layers, self.tensor.size(0), self.hidden_size)
        if self.method == "xavier":
            return nn.init.xavier_normal_(self.p_h)
        else:
            return self.p_h