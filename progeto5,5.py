import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import datetime, timedelta

class TarefaManager:
    def __init__(self):
        self.tarefas = []

    def adicionar_tarefa(self, descricao, prazo=None):
        if descricao:
            data_criacao = datetime.now()
            self.tarefas.append({"descricao": descricao, "data_criacao": data_criacao, "prazo": prazo, "concluida": False})
            return True
        else:
            return False

    def remover_tarefa(self, indice):
        if 0 <= indice < len(self.tarefas):
            del self.tarefas[indice]

    def alterar_estado_tarefa(self, indice, concluida=True):
        if 0 <= indice < len(self.tarefas):
            self.tarefas[indice]["concluida"] = concluida

    def obter_tarefas_formatadas(self, concluidas=None):
        if concluidas is None:
            return [f"{i}. {tarefa['descricao']} - Prazo: {tarefa['prazo']}" for i, tarefa in enumerate(self.tarefas, 1)]
        else:
            return [f"{i}. {tarefa['descricao']} - Prazo: {tarefa['prazo']}" for i, tarefa in enumerate(self.tarefas, 1) if tarefa['concluida'] == concluidas]

    def formatar_tempo(self, tempo):
        agora = datetime.now()
        diferenca = agora - tempo

        if diferenca < timedelta(minutes=1):
            return "há alguns segundos"
        elif diferenca < timedelta(hours=1):
            minutos = diferenca.seconds // 60
            return f"há {minutos} minutos"
        elif diferenca < timedelta(days=1):
            horas = diferenca.seconds // 3600
            return f"há {horas} horas"
        else:
            return tempo.strftime("%d/%m/%Y %H:%M:%S")

class GerenciadorTarefasApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Gerenciador de Tarefas")
        self.tarefa_manager = TarefaManager()

        # Widgets
        self.label = tk.Label(master, text="Nova Tarefa:")
        self.label.pack(pady=10)

        self.entry_tarefa = tk.Entry(master, width=30)
        self.entry_tarefa.pack()

        self.label_prazo = tk.Label(master, text="Prazo (opcional - formato: dd/mm/yyyy HH:MM):")
        self.label_prazo.pack()

        self.entry_prazo = tk.Entry(master, width=30)
        self.entry_prazo.pack()

        self.botao_adicionar = tk.Button(master, text="Adicionar Tarefa", command=self.adicionar_tarefa)
        self.botao_adicionar.pack(pady=10)

        self.botao_remover = tk.Button(master, text="Remover Tarefa", command=self.remover_tarefa)
        self.botao_remover.pack(pady=5)

        self.botao_exportar = tk.Button(master, text="Exportar", command=self.exportar_tarefas)
        self.botao_exportar.pack(pady=5)

        self.notebook = ttk.Notebook(master)
        self.notebook.pack(pady=10)

        self.frame_nao_concluidas = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_nao_concluidas, text='Não Concluídas')

        self.frame_concluidas = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_concluidas, text='Concluídas')

        self.tree_tarefas_nao_concluidas = ttk.Treeview(self.frame_nao_concluidas, columns=('Descrição', 'Prazo', 'Data de Criação'), show='headings')
        self.tree_tarefas_nao_concluidas.heading('Descrição', text='Descrição')
        self.tree_tarefas_nao_concluidas.heading('Prazo', text='Prazo')
        self.tree_tarefas_nao_concluidas.heading('Data de Criação', text='Data de Criação')
        self.tree_tarefas_nao_concluidas.pack(side='left', fill='both', expand=True)

        self.tree_tarefas_concluidas = ttk.Treeview(self.frame_concluidas, columns=('Descrição', 'Prazo', 'Data de Criação'), show='headings')
        self.tree_tarefas_concluidas.heading('Descrição', text='Descrição')
        self.tree_tarefas_concluidas.heading('Prazo', text='Prazo')
        self.tree_tarefas_concluidas.heading('Data de Criação', text='Data de Criação')
        self.tree_tarefas_concluidas.pack(side='right', fill='both', expand=True)

        self.botao_concluir = tk.Button(master, text="Concluir", command=self.concluir_tarefa)
        self.botao_concluir.pack(pady=5)

        self.botao_desfazer_conclusao = tk.Button(master, text="Desfazer Conclusão", command=self.desfazer_conclusao_tarefa)
        self.botao_desfazer_conclusao.pack(pady=5)

        self.label_editar_tarefa = tk.Label(master, text="Editar Tarefa:")
        self.label_editar_tarefa.pack(pady=10)

        self.entry_editar_tarefa = tk.Entry(master, width=30)
        self.entry_editar_tarefa.pack()

        self.botao_editar_tarefa = tk.Button(master, text="Editar Tarefa", command=self.editar_tarefa)
        self.botao_editar_tarefa.pack(pady=5)

        # Iniciar a atualização periódica
        self.atualizar_periodicamente()

    def adicionar_tarefa(self):
        descricao = self.entry_tarefa.get()
        prazo = self.entry_prazo.get()
        if self.tarefa_manager.adicionar_tarefa(descricao, prazo):
            self.atualizar_listas_tarefas()
            self.mostrar_mensagem("Tarefa adicionada com sucesso.")
            self.limpar_campos_entrada()

    def remover_tarefa(self):
        indice_selecionado = self.obter_indice_selecionado(self.tree_tarefas_nao_concluidas)
        if indice_selecionado is not None:
            self.tarefa_manager.remover_tarefa(indice_selecionado)
            self.atualizar_listas_tarefas()

    def concluir_tarefa(self):
        indice_selecionado = self.obter_indice_selecionado(self.tree_tarefas_nao_concluidas)
        if indice_selecionado is not None:
            self.tarefa_manager.alterar_estado_tarefa(indice_selecionado, concluida=True)
            self.atualizar_listas_tarefas()

    def desfazer_conclusao_tarefa(self):
        indice_selecionado = self.obter_indice_selecionado(self.tree_tarefas_concluidas)
        if indice_selecionado is not None:
            self.tarefa_manager.alterar_estado_tarefa(indice_selecionado, concluida=False)
            self.atualizar_listas_tarefas()

    def editar_tarefa(self):
        indice_selecionado = self.obter_indice_selecionado(self.tree_tarefas_nao_concluidas)
        if indice_selecionado is not None:
            nova_descricao = self.entry_editar_tarefa.get()
            if nova_descricao:
                self.tarefa_manager.tarefas[indice_selecionado]["descricao"] = nova_descricao
                self.atualizar_listas_tarefas()
                self.mostrar_mensagem("Tarefa editada com sucesso.")
                self.limpar_campos_entrada()
            else:
                self.mostrar_mensagem("A descrição não pode estar vazia.")

    def exportar_tarefas(self):
        arquivo = filedialog.asksaveasfilename(defaultextension=".csv")
        with open(arquivo, "w") as f:
            f.write("Descrição,Prazo\n")
            for tarefa in self.tarefa_manager.tarefas:
                f.write(f"{tarefa['descricao']},{tarefa['prazo']}\n")

    def atualizar_periodicamente(self):
        self.atualizar_listas_tarefas()
        self.master.after(60000, self.atualizar_periodicamente)

    def atualizar_listas_tarefas(self):
        self.limpar_treeview(self.tree_tarefas_nao_concluidas)
        self.limpar_treeview(self.tree_tarefas_concluidas)

        tarefas_nao_concluidas_formatadas = self.tarefa_manager.obter_tarefas_formatadas(concluidas=False)
        self.preencher_treeview(self.tree_tarefas_nao_concluidas, tarefas_nao_concluidas_formatadas)

        tarefas_concluidas_formatadas = self.tarefa_manager.obter_tarefas_formatadas(concluidas=True)
        self.preencher_treeview(self.tree_tarefas_concluidas, tarefas_concluidas_formatadas)

        self.configurar_cores_treeview(self.tree_tarefas_nao_concluidas, 'atrasada', background='red')
        self.configurar_cores_treeview(self.tree_tarefas_nao_concluidas, 'proxima', background='yellow')
        self.configurar_cores_treeview(self.tree_tarefas_concluidas, 'concluida', background='green')

def exibir_janela_visualizar_tarefas(self):
        visualizar_tarefas_root = tk.Toplevel(self.master)
        visualizar_tarefas_app = 'VisualizaTarefasApp'(visualizar_tarefas_root, self.tarefa_manager)

def mostrar_mensagem(self, mensagem):
        messagebox.showinfo("Aviso", mensagem)

def limpar_campos_entrada(self):
        self.entry_tarefa.delete(0, tk.END)
        self.entry_prazo.delete(0, tk.END)

def obter_indice_selecionado(self, treeview):
        indice_selecionado = treeview.selection()
        if indice_selecionado:
            return int(treeview.item(indice_selecionado, 'text')) - 1
        return None
def limpar_treeview(self, treeview):
        treeview.delete(*treeview.get_children())

def preencher_treeview(self, treeview, tarefas_formatadas):
        for i, tarefa_formatada in enumerate(tarefas_formatadas, 1):
            tarefa = self.tarefa_manager.tarefas[i - 1]
            prazo_destacado, tag = self.destacar_prazo(tarefa['prazo'])
            treeview.insert('', 'end', text=str(i), values=(tarefa['descricao'], prazo_destacado, self.tarefa_manager.formatar_tempo(tarefa['data_criacao'])), tags=(tag, 'concluida' if tarefa['concluida'] else ''))

def configurar_cores_treeview(self, treeview, tag, **kwargs):
        treeview.tag_configure(tag, **kwargs)

def destacar_prazo(self, prazo):
        if prazo:
            try:
                prazo_formatado = datetime.strptime(prazo, "%d/%m/%Y %H:%M")
            except ValueError:
                return f"Formato inválido: {prazo}", ''

            agora = datetime.now()
            uma_hora_antes = agora + timedelta(hours=1)
            if agora > prazo_formatado:
                return f"[ATRASADA] {prazo} (Atrasada!)", 'atrasada'
            elif uma_hora_antes > prazo_formatado:
                return f"[PRÓXIMA] {prazo} (Próxima a vencer)", 'proxima'
            else:
                return prazo, ''

class LoginApp:
    def __init__(self, master, on_login_success):
        self.master = master
        self.master.title("Login")
        self.on_login_success = on_login_success

        # Widgets
        self.label_login = tk.Label(master, text="Login:")
        self.label_login.pack(pady=10)

        self.entry_login = tk.Entry(master, width=30)
        self.entry_login.pack()

        self.label_senha = tk.Label(master, text="Senha:")
        self.label_senha.pack()

        self.entry_senha = tk.Entry(master, show="*", width=30)
        self.entry_senha.pack()

        self.botao_login = tk.Button(master, text="Login", command=self.fazer_login)
        self.botao_login.pack(pady=10)

    def fazer_login(self):
        login = self.entry_login.get()
        senha = self.entry_senha.get()

        # Verificar se o login e senha estão corretos
        if login == "leo" and senha == "123":
            self.master.destroy()  # Fechar a janela de login
            self.on_login_success()  # Chamar a função de sucesso de login
        else:
            messagebox.showerror("Erro de Login", "Login ou senha incorretos.")

if __name__ == "__main__":
    def iniciar_gerenciador_tarefas():
        root = tk.Tk()
        gerenciador_tarefas_app = GerenciadorTarefasApp(root)
        root.mainloop()

    root_login = tk.Tk()
    login_app = LoginApp(root_login, on_login_success=iniciar_gerenciador_tarefas)
    root_login.mainloop()
