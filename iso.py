import os
import pycdlib
try:
    from cStringIO import StringIO as BytesIO
except ImportError:
    from io import BytesIO

def parse_tree(file_path):
    tree = {}
    current_path = []
    
    with open(file_path, 'r') as file:
        for line in file:
            line = line.rstrip()
            if not line.strip():  # Ignora linhas vazias
                continue
            
            indent_level = len(line) - len(line.lstrip())
            node = line.strip()
            
            # Atualiza o nível atual
            while len(current_path) > indent_level:
                current_path.pop()
            
            # Adiciona o nó à árvore
            current_tree = tree
            for part in current_path:
                current_tree = current_tree[part]
            
            if '=' in node:
                name, content = node.split('=', 1)
                current_tree[name] = content.replace('\\n', '\n').replace('\\r', '\r')
            else:
                current_tree[node] = {}
                current_path.append(node)
    
    return tree

def add_to_iso(iso, tree, base_path='/'):
    for name, content in tree.items():
        if isinstance(content, dict):
            # Diretório
            dir_path = os.path.join(base_path, name)
            iso.add_directory(dir_path.upper())
            add_to_iso(iso, content, dir_path)
        else:
            # Ficheiro
            file_path = os.path.join(base_path, name).replace("\\","/")
            print(file_path)
            iso.add_fp(BytesIO(content.encode()), len(content), file_path.upper())

def main():
    input_file = input("Insira o nome do ficheiro de entrada (.txt): ").strip()
    if not os.path.isfile(input_file):
        print("Ficheiro não encontrado!")
        return
    
    tree = parse_tree(input_file)
    output_iso = os.path.splitext(input_file)[0] + ".iso"
    
    iso = pycdlib.PyCdlib()
    iso.new(interchange_level=3)

    add_to_iso(iso, tree)

    iso.write(output_iso)
    iso.close()
    print(f"Imagem ISO criada: {output_iso}")

if __name__ == "__main__":
    main()

