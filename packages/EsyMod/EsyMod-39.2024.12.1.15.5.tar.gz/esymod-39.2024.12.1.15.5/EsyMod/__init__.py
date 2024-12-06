import torch
import EsyPro
import torch.utils
import torch.utils.data
class Model(torch.nn.Sequential):
    """
    1. model with device param for device automatic adaptation.
    2. model with save and load method for model persistence.
    3. model with param_num property for model parameter count.
    4. model with output property for forward output.
    """
    
    def __init__(self, *layers):
        """
        init model with layers.
        """
        super().__init__()
        for idx, module in enumerate(layers):
            self.add_module(f'layer{idx}', module)
    
    def get_output(self, x):
        return super().forward(x)
        
    def forward(self, *args, **kwargs):
        """
        forward pass

        Args:
            x (Tensor): input tensor

        Returns:
            Tensor: output tensor
        """
        self.output = self.get_output(*args, **kwargs)
        return self.output

    #region device
    @ property
    def device(self):
        return next(self.parameters()).device
    #endregion

    #region param count
    @ property
    def param_num(self):
        params = list(self.parameters())
        k = 0
        for i in params:
            l = 1
            for j in i.size():
                l *= j
            k = k + l
        return k
    #endregion

import copy
class Dataset(torch.utils.data.Dataset):
    """
    A custom dataset class that extends `torch.utils.data.Dataset` to handle tensor data and provide additional functionality such as iteration, data loading, and k-fold cross-validation. \n
    **Attributes**:\n
        sample_selection (torch.Tensor): A tensor containing the indices of the samples to be used.\n
        tensors (list of torch.Tensor): A list of tensors containing the data.\n
    **Methods**:\n
        __init__(self, tensors, sample_selection=None):\n
            Initializes the dataset with the given tensors and optional sample selection.\n
        __iter__(self):\n
            Initializes the iterator for the dataset.\n
        __next__(self):\n
            Returns the next item in the dataset during iteration.\n
        get_loader(self, batch_size=4, shuffle=True):\n
            Returns a DataLoader for the dataset with the specified batch size and shuffle option.\n
        __getitem__(self, select_index):\n
            Returns the item at the specified index.\n
        __len__(self):\n
            Returns the length of the dataset.\n
        subset(self, sample_selection):\n
            Creates a copy of the dataset with a new sample selection.\n
        k_split(self, k):\n
            Splits the dataset into k folds for cross-validation and returns a list of (train_subset, val_subset) tuples.
    """
    def __init__(self, tensors, sample_selection=None):
        """
        Initializes the dataset with the given tensors and optional sample selection.
        Args:
            tensors (list of torch.Tensor): A list of tensors containing the data.
            sample_selection (torch.Tensor): A tensor containing the indices of the samples to be used.
        """
        if sample_selection is None:
            sample_selection = torch.arange(len(tensors[0]))
        self.sample_selection = sample_selection
        self.tensors = tensors

    #region iterable
    def __iter__(self):
        self.iter_count = -1
        return self

    def __next__(self):
        self.iter_count += 1
        if self.iter_count >= len(self):
            raise StopIteration
        return self[self.iter_count]
    #endregion

    def get_loader(self, batch_size=4, shuffle=True):
        """
        Returns a DataLoader for the dataset with the specified batch size and shuffle option.
        Args:
            batch_size (int): The batch size for the DataLoader.
            shuffle (bool): Whether to shuffle the data.
        Returns:
            (DataLoader): A DataLoader for the dataset.
        """
        return torch.utils.data.DataLoader(self, batch_size=batch_size, shuffle=shuffle)

    def __getitem__(self, select_index):
        index = self.sample_selection[select_index].item()
        result = []
        for tensor in self.tensors:
            result.append(tensor[index])
        return result

    def __len__(self):
        return len(self.sample_selection)
    
    def subset(self, sample_selection):
        """
        拷贝一个共享所有属性的数据集，单独替换sample_selection
        Args:
            sample_selection (torch.Tensor): A tensor containing the indices of the samples to be used.
        Returns:
            (Dataset): A copy of the dataset with the new sample selection.
        """
        copyset = copy.copy(self)
        copyset.sample_selection = sample_selection
        return copyset
    
    def k_split(self, k, shuffle=True):
        """
        按照k折划分验证的要求，返回交叉验证数据集.
        Args:
            k (int): The number of folds for cross-validation.
        Returns:
            (Dataset, Dataset): A list of (train_subset, val_subset) tuples.
        """
        total_index = torch.arange(len(self))
        # shuffle
        if shuffle:
            total_index = total_index[torch.randperm(len(total_index))]
        
        # split
        subsets = []
        for i in range(k):
            val_index = total_index[i::k]
    
            train_index = total_index[~torch.isin(total_index, val_index)]
            # sort
            val_index, _ = val_index.sort()
            train_index, _ = train_index.sort()            
            val_subset = self.subset(val_index)
            train_subset = self.subset(train_index)
            subsets.append((train_subset, val_subset))
        
        
        return subsets
    
        
