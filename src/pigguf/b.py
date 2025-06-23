
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

def list_gguf_files():
    return [f for f in os.listdir() if f.endswith(".gguf")]

def brush_tensor(input_path, tensor_name, output_path="output.gguf"):
    with open(input_path, "rb") as f:
        reader = GGUFReader(f)
        arch = get_arch_str(reader)
        file_type = get_file_type(reader)
        print(f"Detected architecture: '{arch}' (file type: {file_type})")
        writer = GGUFWriter(path=None, arch=arch)
        writer.add_quantization_version(GGML_QUANT_VERSION)
        writer.add_file_type(file_type)
        for tensor in reader.tensors:
            if tensor.name == tensor_name:
                print(f"Skipping tensor: {tensor.name}")
                continue
            writer.add_tensor(tensor.name, tensor.data, raw_dtype=tensor.tensor_type)
        with open(output_path, "wb"):
            writer.write_header_to_file(path=output_path)
            writer.write_kv_data_to_file()
            writer.write_tensors_to_file(progress=True)
            writer.close()

def tensor_brush():
    gguf_files = list_gguf_files()
    if not gguf_files:
        print("No .gguf files found in the current directory.")
        return
    print("Available GGUF files:")
    for idx, f in enumerate(gguf_files):
        print(f"{idx + 1}. {f}")
    choice = int(input("Select the input GGUF file by number: ")) - 1
    input_file = gguf_files[choice]
    with open(input_file, "rb") as f:
        reader = GGUFReader(f)
        print("\nTensors in the file:")
        for idx, tensor in enumerate(reader.tensors):
            print(f"{idx + 1}. {tensor.name} — shape: {tensor.shape}, dtype: {tensor.tensor_type}")
    tensor_idx = int(input("\nSelect the tensor to REMOVE by number: ")) - 1
    tensor_name = reader.tensors[tensor_idx].name
    brush_tensor(input_file, tensor_name)
    print(f"\nTensor '{tensor_name}' removed. Output saved as 'output.gguf'.")

def main():
    tensor_brush()

if __name__ == '__main__':
    main()
