from django.db import models
from django.conf import settings
import qrcode
import json
from io import BytesIO
from django.core.files import File
from pypdf import PdfReader 

class Produtos(models.Model):
    nome = models.CharField(max_length=255)
    dono = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    descricao = models.TextField()
    
    # Novo campo para o PDF (aceita apenas PDFs)
    arquivo_certificacao = models.FileField(upload_to='certificados/', blank=True, null=True)
    
    # O certificado agora é automático (começa False)
    certificado = models.BooleanField(default=False)
    
    qr_code = models.ImageField(upload_to='qrcodes/', blank=True)

    def __str__(self):
        return self.nome
    
    def save(self, *args, **kwargs):
        # === LOGICA 1: O ALGORITMO DE LEITURA DE PDF ===
        if self.arquivo_certificacao:
            try:
                # 1. Garante que o arquivo está aberto no começo
                self.arquivo_certificacao.open('rb') 
                leitor_pdf = PdfReader(self.arquivo_certificacao)
                texto_completo = ""
                
                # 2. Lê todas as páginas
                for pagina in leitor_pdf.pages:
                    texto_completo += pagina.extract_text()
                
                # === O ESPIÃO (Olhe no seu terminal depois de salvar!) ===
                print(f"--- TEXTO LIDO DO PDF ({self.nome}) ---")
                print(texto_completo)
                print("------------------------------------------")

                # 3. A REGRA DE OURO (Com limpeza)
                # Removemos quebras de linha para evitar erros de formatação
                texto_limpo = texto_completo.replace("\n", " ").replace("  ", " ")
                
                # [cite_start]Verificamos a frase chave (tem que estar idêntica ao PDF válido [cite: 10])
                if "CODIGO-AUTENTICIDADE: VERDE-2024" in texto_limpo:
                    self.certificado = True
                    print(f"RESULTADO: APROVADO ✅")
                else:
                    self.certificado = False
                    print(f"RESULTADO: REPROVADO ❌ (Chave não encontrada)")
                    
            except Exception as e:
                print(f"Erro Crítico ao ler PDF: {e}")
                self.certificado = False
        else:
            self.certificado = False

        # === LOGICA 2: O QR CODE COM JSON ===
        if not self.pk:
            super().save(*args, **kwargs)

        dados_produto = {
            "id": self.pk,
            "nome": self.nome,
            "descricao": self.descricao,
            "certificado_valido": self.certificado,
            "dono": self.dono.username if self.dono else "Desconhecido"
        }

        json_string = json.dumps(dados_produto, indent=4, ensure_ascii=False)
        imagem_qr = qrcode.make(json_string)
        
        buffer = BytesIO()
        imagem_qr.save(buffer)
        buffer.seek(0)
        
        # Gera um nome aleatório ou único para evitar cache de imagem antiga
        import time
        nome_arquivo_qr = f'{self.nome}_v{int(time.time())}.png'
        
        self.qr_code.save(nome_arquivo_qr, File(buffer), save=False)

        super().save(*args, **kwargs)