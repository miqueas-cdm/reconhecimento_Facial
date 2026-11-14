import os
import time
import cv2
import numpy as np

# Silenciar avisos internos do OpenCV DNN
cv2.utils.logging.setLogLevel(cv2.utils.logging.LOG_LEVEL_ERROR)

# Diretório base e caminhos dos modelos ONNX
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
YUNET_MODEL = os.path.join(BASE_DIR, "face_detection_yunet_2023mar.onnx")
SFACE_MODEL = os.path.join(BASE_DIR, "face_recognition_sface_2021dec.onnx")

print("--- SISTEMA DE RECONHECIMENTO FACIAL ---", flush=True)
print("Carregando modelos de inteligência artificial...", flush=True)

# Inicialização dos modelos neurais (YuNet para detecção e SFace para reconhecimento)
detector = cv2.FaceDetectorYN.create(
    model=YUNET_MODEL,
    config="",
    input_size=(320, 320),
    score_threshold=0.6,
    nms_threshold=0.3,
    top_k=5000
)

recognizer = cv2.FaceRecognizerSF.create(
    model=SFACE_MODEL,
    config=""
)

# Imagens de referência para cadastro do rosto
rostos_conhecidos = [
    ("Miqueas", os.path.join(BASE_DIR, "Miqueas01.jpeg")),
    ("Miqueas", os.path.join(BASE_DIR, "Miqueas.jpeg"))
]

encodings_conhecidos = []
nomes_conhecidos = []

print("Cadastrando rostos a partir das imagens...", flush=True)
for nome, caminho in rostos_conhecidos:
    if not os.path.exists(caminho):
        print(f"[!] Imagem não encontrada: {os.path.basename(caminho)}", flush=True)
        continue

    img = cv2.imread(caminho)
    if img is None:
        continue

    h, w, _ = img.shape
    detector.setInputSize((w, h))
    _, faces = detector.detect(img)

    if faces is not None and len(faces) > 0:
        face_aligned = recognizer.alignCrop(img, faces[0])
        feature = recognizer.feature(face_aligned)
        encodings_conhecidos.append(feature)
        nomes_conhecidos.append(nome)
        print(f"[+] Rosto cadastrado com sucesso: {nome} ({os.path.basename(caminho)})", flush=True)
    else:
        print(f"[-] Nenhum rosto detectado na foto: {os.path.basename(caminho)}", flush=True)

if not encodings_conhecidos:
    print("[!] ATENÇÃO: Nenhum rosto de referência foi carregado com sucesso.", flush=True)
else:
    print(f"[OK] Total de referências carregadas: {len(encodings_conhecidos)}", flush=True)

# Inicializa captura da webcam
print("Iniciando webcam (índice 0)...", flush=True)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("[ERRO] Não foi possível acessar a webcam.", flush=True)
    exit(1)

COSINE_THRESHOLD = 0.363  # Limiar padrão do SFace (>= 0.363 indica mesma pessoa)
prev_time = time.time()
fps = 0

print("\n>>> Câmera ativa! Pressione 'q' ou 'ESC' na janela do vídeo para sair. <<<\n", flush=True)

while True:
    ret, frame = cap.read()
    if not ret or frame is None:
        print("[!] Falha na leitura do frame da câmera.", flush=True)
        break

    h, w, _ = frame.shape
    detector.setInputSize((w, h))

    # Detecção facial
    _, faces = detector.detect(frame)

    if faces is not None:
        for face in faces:
            # Caixa delimitadora
            x, y, box_w, box_h = face[0:4].astype(int)

            # Alinhamento e extração de características faciais (embedding 128D)
            face_aligned = recognizer.alignCrop(frame, face)
            face_feature = recognizer.feature(face_aligned)

            # Comparação com rostos conhecidos
            nome_detectado = "Desconhecido"
            maior_similaridade = -1.0

            for enc, nome in zip(encodings_conhecidos, nomes_conhecidos):
                score = recognizer.match(face_feature, enc, cv2.FaceRecognizerSF_FR_COSINE)
                if score > maior_similaridade:
                    maior_similaridade = score
                    if score >= COSINE_THRESHOLD:
                        nome_detectado = nome

            # Estilo visual: Verde para rosto reconhecido, Vermelho para desconhecido
            if nome_detectado != "Desconhecido":
                cor = (0, 220, 0)
                label = f"{nome_detectado} ({maior_similaridade:.2f})"
            else:
                cor = (0, 0, 255)
                label = "Desconhecido"

            # Desenha retângulo e nome
            cv2.rectangle(frame, (x, y), (x + box_w, y + box_h), cor, 2)
            cv2.putText(
                frame,
                label,
                (x, max(25, y - 10)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.75,
                cor,
                2
            )

    # Cálculo e exibição do FPS
    curr_time = time.time()
    fps = 0.9 * fps + 0.1 * (1.0 / max(0.001, curr_time - prev_time))
    prev_time = curr_time
    cv2.putText(
        frame,
        f"FPS: {fps:.1f}",
        (15, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2
    )

    # Exibe imagem na janela
    cv2.imshow("Reconhecimento Facial - Pressione 'q' para sair", frame)

    # Encerra ao pressionar 'q' ou 'ESC'
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q') or key == 27:
        break

cap.release()
cv2.destroyAllWindows()
print("\nPrograma encerrado com sucesso.", flush=True)