import gitlab
import os
import subprocess
import shutil
from datetime import datetime
from dotenv import load_dotenv

# Carrega variáveis
load_dotenv()

# --- CONFIGURAÇÕES ---
GITLAB_URL = os.getenv('GITLAB_URL', 'https://gitlab.maxia.education/')
TOKEN = os.getenv('GITLAB_TOKEN')
GROUP_IDS_STRING = os.getenv('GITLAB_GROUP_IDS', '248;240;229;124')
BASE_DIR = os.getenv('BACKUP_BASE_DIR', r"C:\Users\alyss\OneDrive\Documentos\EduKAI\src\backups_gitlab")

if not TOKEN:
    raise ValueError("❌ ERRO: GITLAB_TOKEN não definido. Verifique seu arquivo .env")
# ---------------------

def main():
    # 1. Conexão
    try:
        gl = gitlab.Gitlab(GITLAB_URL, private_token=TOKEN)
        gl.auth()
        print(f"✅ Conectado como: {gl.user.username}")
    except Exception as e:
        print(f"❌ Erro de autenticação: {e}")
        return

    # 2. Menu
    print("\n" + "="*40)
    print(" SELECIONE O TIPO DE BACKUP")
    print("="*40)
    print(" [1] SNAPSHOT (ZIP) - Apenas arquivos (Leve/Rápido)")
    print(" [2] MIRROR (GIT)   - Histórico Completo (Pesado/Seguro)")
    print("="*40)
    
    choice = input("Opção (1 ou 2): ").strip()
    if choice == '1':
        backup_type = "Snapshot"
    elif choice == '2':
        backup_type = "Mirror"
    else:
        print("Opção inválida.")
        return

    # 3. Prepara pastas
    data_hoje = datetime.now().strftime('%Y-%m-%d')
    daily_path = os.path.join(BASE_DIR, data_hoje, backup_type)

    group_ids = [gid.strip() for gid in GROUP_IDS_STRING.split(';') if gid.strip()]
    print(f"\n🚀 Iniciando backup de {len(group_ids)} grupos em: {daily_path}")

    for gid in group_ids:
        try:
            group = gl.groups.get(int(gid))
            group_path = os.path.join(daily_path, group.name)
            os.makedirs(group_path, exist_ok=True)

            print(f"\n📂 GRUPO: {group.name} (ID: {gid})")
            
            # Pega lista parcial
            projects_list = group.projects.list(all=True)
            print(f"   Encontrados {len(projects_list)} projetos.")

            for partial_project in projects_list:
                print(f"   ⬇️  Processando: {partial_project.name}...", end=" ")
                
                try:
                    # Traz o objeto COMPLETO (Correção principal)
                    full_project = gl.projects.get(partial_project.id)
                    
                    # --- LÓGICA DO ZIP (SNAPSHOT) ---
                    if choice == '1':
                        file_path = os.path.join(group_path, f"{full_project.name}.zip")
                        
                        # Verifica se repo está vazio antes de tentar baixar
                        if full_project.empty_repo:
                            print("⚠️  (Pulado: Repositório Vazio)")
                            continue

                        # Faz download em CHUNKS (Stream) para não estourar a memória RAM
                        try:
                            with open(file_path, 'wb') as f:
                                full_project.repository_archive(format='zip', streamed=True, action=f.write)
                            print("✅ (ZIP Salvo)")
                        except gitlab.exceptions.GitlabGetError:
                            print("❌ (Erro 404/Vazio ao gerar ZIP)")

                    # --- LÓGICA DO MIRROR (GIT) ---
                    elif choice == '2':
                        project_git_path = os.path.join(group_path, f"{full_project.name}.git")
                        repo_url = full_project.http_url_to_repo.replace("https://", f"https://oauth2:{TOKEN}@")

                        # Se a pasta já existe (re-execução), apaga para garantir integridade ou pula
                        if os.path.exists(project_git_path):
                            # Opção A: Apagar e baixar de novo (Mais seguro para garantir mirror limpo)
                            # shutil.rmtree(project_git_path) 
                            
                            # Opção B: Apenas avisar e pular (Mais rápido)
                             print("⚠️  (Já existe, pulando)")
                             continue

                        subprocess.run(
                            ["git", "clone", "--mirror", repo_url, project_git_path],
                            check=True,
                            stdout=subprocess.DEVNULL, 
                            stderr=subprocess.DEVNULL
                        )
                        print("✅ (Mirror Concluído)")

                except Exception as ep:
                    print(f"\n   ❌ Falha individual em {partial_project.name}: {ep}")

        except Exception as eg:
            print(f"\n❌ Erro crítico no Grupo ID {gid}: {eg}")

    print("\n🏁 Backup finalizado.")

if __name__ == "__main__":
    main()