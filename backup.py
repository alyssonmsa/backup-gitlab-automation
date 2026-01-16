import gitlab
import os
import subprocess
from datetime import datetime
from dotenv import load_dotenv

# variáveis de ambiente do arquivo .env
load_dotenv()

# --- CONFIGURAÇÕES ---
GITLAB_URL = os.getenv('GITLAB_URL', 'https://gitlab.maxia.education/')
TOKEN = os.getenv('GITLAB_TOKEN')
GROUP_IDS_STRING = os.getenv('GITLAB_GROUP_IDS', '248;240;229;124')

# Caminho base (Raiz dos backups)
BASE_DIR = os.getenv('BACKUP_BASE_DIR', r"C:\Users\alyss\OneDrive\Documentos\EduKAI\src\backups_gitlab")


if not TOKEN:
    raise ValueError("GITLAB_TOKEN não está definido nas variáveis de ambiente. Configure o arquivo .env")
# ---------------------

def main():
    # 1. Configura conexão
    try:
        gl = gitlab.Gitlab(GITLAB_URL, private_token=TOKEN)
        gl.auth()
        print(f"Conectado como: {gl.user.username}")
    except Exception as e:
        print(f"Erro de autenticação: {e}")
        return

    # 2. Menu de Escolha
    print("\n" + "="*40)
    print(" SELECIONE O TIPO DE BACKUP")
    print("="*40)
    print(" [1] SNAPSHOT (ZIP) - Apenas arquivos atuais (sem histórico)")
    print(" [2] MIRROR (GIT)   - Repositório completo (com histórico/branches)")
    print("="*40)
    
    choice = input("Digite a opção (1 ou 2): ").strip()

    if choice == '1':
        backup_type = "Snapshot"
        print("\n>> Modo escolhido: SNAPSHOT (ZIP)")
    elif choice == '2':
        backup_type = "Mirror"
        print("\n>> Modo escolhido: MIRROR (Git Clone)")
    else:
        print("Opção inválida. Saindo.")
        return

    # 3. Prepara Diretório Base do Dia
    data_hoje = datetime.now().strftime('%Y-%m-%d')
    daily_path = os.path.join(BASE_DIR, data_hoje, backup_type)

    # 4. Processa a lista de IDs
    group_ids = [gid.strip() for gid in GROUP_IDS_STRING.split(';') if gid.strip()]

    print(f"\nIniciando processamento de {len(group_ids)} grupos...")

    for gid in group_ids:
        try:
            # Pega o grupo
            group = gl.groups.get(int(gid))
            
            # Cria pasta do grupo
            group_path = os.path.join(daily_path, group.name)
            os.makedirs(group_path, exist_ok=True)

            print(f"\n📂 GRUPO: {group.name} (ID: {gid})")
            print(f"   Salvando em: {group_path}")

            # Lista projetos (objetos parciais/resumidos)
            projects_list = group.projects.list(all=True)
            print(f"   Encontrados {len(projects_list)} projetos.")

            for partial_project in projects_list:
                print(f"   ⬇️  Baixando: {partial_project.name}...", end=" ")
                
                try:
                    # --- CORREÇÃO AQUI ---
                    # Convertemos o objeto parcial em completo para ter acesso a todas as funções
                    full_project = gl.projects.get(partial_project.id)
                    
                    if choice == '1': # ZIP
                        file_path = os.path.join(group_path, f"{full_project.name}.zip")
                        
                        # Agora chamamos repository_archive no objeto completo
                        zip_content = full_project.repository_archive(format='zip')
                        with open(file_path, 'wb') as f:
                            f.write(zip_content)
                        print("✅ (ZIP salvo)")

                    elif choice == '2': # MIRROR
                        # Para mirror, usamos o full_project também para garantir
                        repo_url = full_project.http_url_to_repo.replace("https://", f"https://oauth2:{TOKEN}@")
                        project_git_path = os.path.join(group_path, f"{full_project.name}.git")
                        
                        subprocess.run(
                            ["git", "clone", "--mirror", repo_url, project_git_path],
                            check=True,
                            stdout=subprocess.DEVNULL, 
                            stderr=subprocess.DEVNULL
                        )
                        print("✅ (Mirror concluído)")

                except Exception as ep:
                    print(f"\n   ❌ Falha no projeto {partial_project.name}: {ep}")

        except Exception as eg:
            print(f"\n❌ Erro ao acessar grupo ID {gid}: {eg}")

    print("\n" + "="*40)
    print(" PROCESSO FINALIZADO")
    print("="*40)

if __name__ == "__main__":
    main()