# Reconhecimento Facial

Este projeto implementa um sistema de reconhecimento facial em tempo real usando Python, OpenCV e modelos ONNX para detecção e identificação de rostos. Ele captura imagens da webcam, localiza rostos na cena, compara com imagens de referência cadastradas e exibe o nome da pessoa reconhecida.

## Visão geral

O fluxo principal funciona assim:

1. Carrega os modelos de IA:
   - YuNet para detecção de rostos
   - SFace para extração e comparação de embeddings faciais
2. Lê imagens de referência do diretório do projeto
3. Extrai as características dos rostos conhecidos
4. Abre a webcam
5. Detecta rostos em cada frame
6. Compara cada rosto detectado com os rostos cadastrados
7. Exibe o nome do rosto reconhecido ou "Desconhecido"

O código principal está em:

- `Reconhecimento_Facial_Python.py`

## Estrutura do projeto

- `Reconhecimento_Facial_Python.py` — script principal com detecção e reconhecimento facial em tempo real
- `main.py` — script complementar, relacionado a controle de LED em ambiente MicroPython
- `face_detection_yunet_2023mar.onnx` e `face_recognition_sface_2021dec.onnx` — modelos necessários, obtidos separadamente e mantidos fora do Git
- `Miqueas.jpeg` e `Miqueas01.jpeg` — imagens locais de referência, mantidas fora do Git por conterem dados biométricos

## Dependências

Este projeto depende dos seguintes itens:

- Python 3.x
- OpenCV (`opencv-python`)
- NumPy
- Webcam conectada ao computador

### Instalação

No terminal, execute:

```bash
pip install opencv-python numpy
```

Depois, coloque na pasta do projeto os dois modelos ONNX com os nomes exatos abaixo:

- `face_detection_yunet_2023mar.onnx`
- `face_recognition_sface_2021dec.onnx`

Obtenha os modelos no [OpenCV Zoo](https://github.com/opencv/opencv_zoo), observando as licenças e condições de uso aplicáveis.

Coloque também na pasta imagens de referência próprias, chamadas `Miqueas.jpeg` e/ou `Miqueas01.jpeg`, ou altere os caminhos no script. Esses arquivos são ignorados pelo Git e não devem ser publicados, pois contêm dados biométricos.

Se o ambiente exigir, também pode ser necessário instalar dependências adicionais do OpenCV conforme a versão do sistema operacional.

## Como executar

A partir da pasta do projeto:

```bash
python Reconhecimento_Facial_Python.py
```

O programa vai:

- carregar os modelos ONNX
- cadastrar os rostos encontrados nas imagens de referência
- iniciar a webcam
- mostrar a tela com os rostos detectados e identificados

## Controles da aplicação

- `q` — fecha a aplicação
- `Esc` — fecha a aplicação

## Como funciona o reconhecimento

O projeto usa duas etapas principais:

### 1. Detecção

O modelo YuNet identifica a localização dos rostos no frame capturado pela câmera.

### 2. Reconhecimento

O modelo SFace gera um vetor de características (embedding) para cada rosto detectado. Em seguida, o sistema compara esse vetor com os embeddings das imagens cadastradas.

Se a similaridade for maior ou igual ao limiar configurado, o rosto é identificado; caso contrário, é marcado como desconhecido.

No código, o limiar usado é:

```python
COSINE_THRESHOLD = 0.363
```

## Observações importantes

- O projeto exige uma webcam disponível e acessível pelo sistema
- Os rostos de referência devem estar em imagens nítidas e bem iluminadas
- A precisão melhora quando as imagens usadas para cadastro têm ângulos e iluminação parecidos com os do uso real
- O reconhecimento é destinado a fins educativos e de demonstração

## Arquivos de referência

Por padrão, o script procura estas imagens locais para cadastrar os rostos:

- `Miqueas.jpeg`
- `Miqueas01.jpeg`

Essas imagens são convertidas em embeddings e comparadas com os rostos da webcam.
Elas não são incluídas no repositório. Para testar, use imagens de referência que você tenha autorização para processar e mantenha-as localmente.

## Script adicional (`main.py`)

O arquivo `main.py` não faz parte do reconhecimento facial em câmera. Ele é um script de controle de LED em ambiente MicroPython, que recebe comandos via entrada padrão e liga/desliga um LED conforme os comandos:

- `OK` → liga o LED
- `OFF` → desliga o LED

Esse arquivo é útil em projetos eletrônicos que combinam lógica de entrada/saída com um microcontrolador.

## Possíveis problemas

Se o programa não funcionar corretamente, verifique:

- se a webcam está conectada e disponível
- se as imagens de referência locais existem na pasta do projeto
- se os modelos ONNX foram obtidos e estão presentes no diretório
- se as bibliotecas Python foram instaladas corretamente
- se há conflito com outra aplicação usando a webcam

## Licença

Este projeto foi desenvolvido como exemplo de uso de visão computacional e reconhecimento facial com OpenCV. Consulte os termos das bibliotecas e dos modelos utilizados antes de uso em produção ou aplicações comerciais.

## Conclusão

Este projeto demonstra como criar um sistema simples de identificação facial em Python usando modelos ONNX de detecção e reconhecimento. É uma base excelente para aprendizado, protótipos e integrações futuras em sistemas de segurança, automação ou controle de acesso.
