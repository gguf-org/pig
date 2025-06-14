
from collections import defaultdict
from gguf_connector.const import GGML_QUANT_VERSION, LlamaFileType
from gguf_connector.reader import GGUFReader
from gguf_connector.writer import GGUFWriter
import os

def get_arch_str(reader):
    field = reader.get_field("general.architecture")
    return str(field.parts[field.data[-1]], encoding="utf-8")

def get_file_type(reader):
    field = reader.get_field("general.file_type")
    ft = int(field.parts[field.data[-1]])
    return LlamaFileType(ft)

def split_by_tensor_dimensions(input_path):
    with open(input_path, "rb") as f:
        reader = GGUFReader(f)
        arch = get_arch_str(reader)
        file_type = get_file_type(reader)
        print(f"Detected arch: '{arch}' (ftype: {str(file_type)})")
        tensors_by_dim = defaultdict(list)
        for tensor in reader.tensors:
            ndim = len(tensor.shape)
            tensors_by_dim[ndim].append(tensor)
        for ndim, tensor_group in tensors_by_dim.items():
            output_path = f"dim{ndim}-extracted.gguf"
            writer = GGUFWriter(path=None, arch=arch)
            writer.add_quantization_version(GGML_QUANT_VERSION)
            writer.add_file_type(file_type)
            print(f"Writing {len(tensor_group)} tensor(s) to {output_path} (dim={ndim})")
            for tensor in tensor_group:
                writer.add_tensor(tensor.name, tensor.data, raw_dtype=tensor.tensor_type)
            with open(output_path, "wb"):
                writer.write_header_to_file(path=output_path)
                writer.write_kv_data_to_file()
                writer.write_tensors_to_file(progress=True)
                writer.close()

def list_gguf_files():
    return [f for f in os.listdir() if f.endswith(".gguf")]

def decompose_gguf():
    gguf_files = list_gguf_files()
    if gguf_files:
        print("GGUF file(s) available. Select which one to split:")
        for index, file_name in enumerate(gguf_files, start=1):
            print(f"{index}. {file_name}")
        choice = input(f"Enter your choice (1 to {len(gguf_files)}): ")
        try:
            choice_index=int(choice)-1
            selected_file=gguf_files[choice_index]
            print(f"Model file: {selected_file} is selected!")
            input_path=selected_file
            split_by_tensor_dimensions(input_path)
        except (ValueError, IndexError):
            print("Invalid choice. Please enter a valid number.")
    else:
        print("No GGUF files are available in the current directory.")
        input("--- Press ENTER To Exit ---")

decompose_gguf()
