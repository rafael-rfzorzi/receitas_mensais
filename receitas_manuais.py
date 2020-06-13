from tkinter import *
from tkinter import ttk
import sqlite3
from datetime import *


root = Tk()

class Funcs():
    def conectabd(self):
        self.conn = sqlite3.connect("receita_manual.db")
        self.cursor = self.conn.cursor()
    def desconectabd(self):
        self.conn.close()
    def montaTabelas(self):
        self.conectabd();
        print("Conectando ao banco de dados")
        ### Cria tabela servprod
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS receitas (
                cod INTEGER PRIMARY KEY,
                obs CHAR(200),
                entrada FLOAT(2,2),
                saida FLOAT(2,2),
                dia INTEGER(4),
                mes INTEGER(4) NOT NULL,
                ano INTEGER(6) NOT NULL
             );
         """)
        self.conn.commit();
        print("banco de dados ja criado")
        self.desconectabd();
        print("desconectando ao banco de dados")
    def limpa_tela(self):
        self.input_ano.delete(0, END)
        self.inp_dia.delete(0, END)
        self.inp_mes.delete(0, END)
        self.inp_obs.delete(0, END)
        self.inp_saida.delete(0, END)
        self.inp_entrada.delete(0, END)

        self.input_ano.insert(END, self.hj.year)
        self.inp_dia.insert(END, self.hj.day)
        self.inp_mes.insert(END, self.hj.month)
        self.inp_obs.insert(END, "")
        self.inp_saida.insert(END, "00.00")
        self.inp_entrada.insert(END, "00.00")

    def variaveis(self):
        self.ano = self.input_ano.get()
        self.dia = self.inp_dia.get()
        self.mes = self.inp_mes.get()
        self.obs = self.inp_obs.get()
        self.entrada = self.inp_entrada.get()
        self.saida = self.inp_saida.get()
    def add_mov(self):
        self.conectabd()
        self.variaveis()

        self.cursor.execute("""
             INSERT INTO receitas ( obs, entrada, saida, dia, mes, ano)
             VALUES ( ?, ?, ?, ?, ?, ?)""",
                            (self.obs, self.entrada, self.saida, self.dia, self.mes, self.ano))
        self.conn.commit()

        self.desconectabd()
        self.select_lista()
        self.limpa_tela()
    def select_lista(self):
        mes_lista = self.corvar.get()
        ano_lista = self.corvar2.get()

        self.lista.delete(*self.lista.get_children())
        self.conectabd()
        lista = self.cursor.execute("""SELECT  entrada, saida, dia, mes , ano, obs FROM receitas  
            WHERE mes = '%s' and ano = '%s' ORDER BY dia ASC; """ % (mes_lista, ano_lista))

        for i in lista:
            self.lista.insert("", END, values=i)

        self.entradas_totais.delete(0, END)
        lista2 = self.cursor.execute("""SELECT  SUM(entrada) FROM receitas  
                    WHERE mes = '%s' and ano = '%s' ORDER BY dia ASC; """ % (mes_lista, ano_lista))


        for i in lista2:
            self.entradas_totais.insert(END, i)

        self.saidas_totais.delete(0, END)
        lista3 = self.cursor.execute("""SELECT  SUM(saida) FROM receitas  
                            WHERE mes = '%s' and ano = '%s' ORDER BY dia ASC; """ % (mes_lista, ano_lista))

        for i in lista3:
            self.saidas_totais.insert(END, i)

        self.saldo_total.delete(0, END)
        lista3 = self.cursor.execute("""SELECT  (SUM(entrada) - SUM(saida)) FROM receitas  
                                    WHERE mes = '%s' and ano = '%s' ORDER BY dia ASC; """ % (mes_lista, ano_lista))

        for i in lista3:
            self.saldo_total.insert(END, i)

        self.desconectabd()
    def deletaItem(self, event):
        self.lista.selection()
        for n in self.lista.selection():
            col1, col2, col3, col4, col5, col6 = self.lista.item(n, 'values')
            self.conectabd()
            self.cursor.execute("""DELETE FROM receitas WHERE entrada = ? AND saida = ? 
                AND dia = ? AND mes = ? AND ano = ? AND obs = ?""", (col1, col2, col3, col4, col5, col6))

            self.conn.commit()
            self.desconectabd()
            self.select_lista()

class Application(Funcs):
    def __init__(self):
        self.hj = date.today()
        self.root = root
        self.tela()
        self.frames()
        self.widgets()
        self.lista_receitas()
        self.montaTabelas()
        self.limpa_tela()
        self.select_lista()
        self.root.mainloop()
    def tela(self):
        self.root.title("Receitas manuais - RfZorzi")
        self.root.configure(background= "lightgray");
        self.root.geometry("1000x600")
        self.root.resizable(TRUE, TRUE);
        self.root.minsize(width=800, height=500)

    def frames(self):
        ###     Primeiro Container da janela
        top = Frame(self.root, bd=2, bg="#383847", highlightbackground='gray65', highlightthickness=1, relief = 'ridge')
        top.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.1)
        self.top = top
        ###     Segundo Container da janela
        top2 = Frame(self.root, bd=2, bg='#383847', highlightbackground='gray65', highlightthickness=1, relief = 'ridge')
        top2.place(relx=0.52, rely=0.16, relwidth=0.46, relheight=0.1)
        self.top2 = top2
        ###     Terceiro Container da janela
        top3 = Frame(self.root, bd=2, bg='white', highlightbackground='gray65', highlightthickness=1, relief = 'ridge')
        top3.place(relx=0.02, rely=0.26, relwidth=0.96, relheight=0.5)
        self.top3 = top3
        ###     Quarto Container da janela
        top4 = Frame(self.root, bd=2, bg='#383847', highlightbackground='gray65', highlightthickness=1, relief = 'ridge')
        top4.place(relx=0.02, rely=0.78, relwidth=0.96, relheight=0.2)
        self.top4 = top4
    def widgets(self):
        self.lb_entrada = Label(self.top, text='Entrada', bg='#383847', fg='white', font=('dyuthi', 10, 'bold'))
        self.lb_entrada.place(relx= 0.05, rely=0.15, relwidth= 0.07)

        self.inp_entrada = Entry(self.top, fg='gray35')
        self.inp_entrada.place(relx=0.05, rely=0.5, relwidth= 0.07)

        self.lb_saida = Label(self.top, text='Saida', bg='#383847', fg='white', font=('dyuthi', 10, 'bold'))
        self.lb_saida.place(relx=0.15, rely=0.15, relwidth= 0.07)

        self.inp_saida = Entry(self.top, fg='gray35')
        self.inp_saida.place(relx=0.15, rely=0.5, relwidth=0.07)

        self.lb_dia = Label(self.top, text = 'Dia', bg='#383847', fg='lightgray',
                            font=('verdana', 9, 'bold')).place(relx=0.35, rely=0.15, relwidth= 0.04)
        self.inp_dia = Entry(self.top, fg='gray35')
        self.inp_dia.place(relx=0.35, rely=0.5, relwidth=0.04)

        self.lb_mes = Label(self.top, text = 'Mês', bg='#383847', fg='lightgray',
                            font=('verdana', 9, 'bold')).place(relx=0.4, rely=0.15, relwidth= 0.04)
        self.inp_mes = Entry(self.top, fg='gray35')
        self.inp_mes.place(relx=0.4, rely=0.5, relwidth=0.04)

        self.lb_ano = Label(self.top, text = 'Ano', bg='#383847', fg='lightgray',
                            font=('verdana', 10, 'bold')).place(relx=0.45, rely=0.15, relwidth= 0.04)
        self.input_ano = Entry(self.top, fg='gray35')
        self.input_ano.place(relx=0.45, rely=0.5, relwidth=0.07)

        self.lb_obs = Label(self.top, text = 'Obs:', bg='#0e76a8', fg='lightgray',
                            font=('dyuthi', 10, 'bold')).place(relx=0.55, rely=0.15, relwidth= 0.07)
        self.inp_obs = Entry(self.top, fg='gray35')
        self.inp_obs.place(relx=0.55, rely=0.5, relwidth=0.3)

        self.bt_inserir = Button(self.top, text= 'Inserir', bg= "#0e76a8",bd = 1, highlightbackground='lightgray',
                    highlightthickness=1, fg="lightgray", font=('verdana', 12, 'bold'),
                    activebackground="#108ecb", activeforeground= "white", command= self.add_mov)
        self.bt_inserir.place(relx=0.9, rely=0.2, relwidth=0.09, relheight=0.6)
        #####
        self.mes_listaLb = Label(self.top2, text= 'Mês', bg= 'gray', fg= 'lightgray',
                                 font=('Verdana', '7', 'bold'))
        self.mes_listaLb.place(relx=0.1, rely=0.19, relwidth=0.2, relheight=0.62)
        self.mesListaEntry = Frame(self.top2, bd=2)
        self.mesListaEntry.grid(column=0, row=0, sticky=(N, W, E, S))
        self.mesListaEntry.columnconfigure(0, weight=1)
        self.mesListaEntry.rowconfigure(0, weight=1)
        self.mesListaEntry.place(relx=0.1, rely=0.1, relwidth=0.3, relheight=0.9)
        self.corvar = StringVar(self.top2)
        self.coresV = {'1', '2', '3', '4', '5', '6', '7', '8', '9',
                       '10', '11', '12'}
        self.corvar.set(self.hj.month)
        self.popupMenu = OptionMenu(self.mesListaEntry, self.corvar, *self.coresV)
        self.popupMenu.grid(row=2, column=1)

        self.mesListaEntry.place(relx=0.1, rely=0.2, relwidth=0.2, relheight=0.6)

        self.ano_listaLb = Label(self.top2, text='Mês', bg='gray', fg='lightgray',
                                 font=('Verdana', '7', 'bold'))
        self.ano_listaLb.place(relx=0.4, rely=0.19, relwidth=0.15, relheight=0.62)
        self.anoListaEntry = Frame(self.top2, bd=2)
        self.anoListaEntry.grid(column=0, row=0, sticky=(N, W, E, S))
        self.anoListaEntry.columnconfigure(0, weight=1)
        self.anoListaEntry.rowconfigure(0, weight=1)
        self.anoListaEntry.place(relx=0.4, rely=0.1, relwidth=0.2, relheight=0.9)
        self.corvar2 = StringVar(self.top2)
        self.coresV2 = {'2020', '2021', '2022'}
        self.corvar2.set(self.hj.year)
        self.popupMenu = OptionMenu(self.anoListaEntry, self.corvar2, *self.coresV2)
        self.popupMenu.grid(row=2, column=1)

        self.anoListaEntry.place(relx=0.4, rely=0.2, relwidth=0.18, relheight=0.64)

        self.bt_select_month = Button(self.top2, text='Seleciona', bg="#0e76a8", bd=1, highlightbackground='lightgray',
                highlightthickness=1, fg="lightgray", font=('verdana', 12, 'bold'), activebackground="#108ecb",
                activeforeground="white", command = self.select_lista)
        self.bt_select_month.place(relx=0.65, rely=0.2, relwidth=0.3, relheight=0.6)

        self.entradas_totaisLb = Label(self.top4, text= 'Total Entrada')
        self.entradas_totaisLb.place(relx=0.08, rely=0.1, relwidth=0.12)
        self.entradas_totais = Entry(self.top4)
        self.entradas_totais.place(relx=0.08, rely=0.3, relwidth= 0.12)

        self.saidas_totaisLb = Label(self.top4, text = 'Total Saida')
        self.saidas_totaisLb.place(relx=0.23, rely=0.1, relwidth=0.12)
        self.saidas_totais = Entry(self.top4)
        self.saidas_totais.place(relx=0.23, rely=0.3, relwidth=0.12)

        self.saldo_totalLb = Label(self.top4, text= 'Saldo')
        self.saldo_totalLb.place(relx=0.68, rely=0.1, relwidth=0.12)
        self.saldo_total = Entry(self.top4)
        self.saldo_total.place(relx=0.68, rely=0.3, relwidth=0.12)
    def lista_receitas(self):
        self.barra = Scrollbar(self.top3, orient='vertical')#, command=self.OnVsb_Orc2)
        self.barra.place(relx=0.98, rely=0.01, relwidth=0.02, relheight=0.97)

        self.lista = ttk.Treeview(self.top3, height=10, yscrollcommand=self.barra.set,
                                           column=("col1", "col2", "col3", "col4", "col5", "col6"))

        self.lista.heading("#0", text="")
        self.lista.heading("#1", text="Entrada")
        self.lista.heading("#2", text="Saida")
        self.lista.heading("#3", text="Dia")
        self.lista.heading("#4", text="Mes")
        self.lista.heading("#5", text="Ano")
        self.lista.heading("#6", text="Obs")

        self.lista.column("#0", width=1)
        self.lista.column("#1", width=100)
        self.lista.column("#2", width=100)
        self.lista.column("#3", width=40)
        self.lista.column("#4", width=40)
        self.lista.column("#5", width=60)
        self.lista.column("#6", width=210)

        self.lista.place(relx=0.0, rely=0.01, relwidth=0.98, relheight=0.94)

        self.lista.configure(yscroll=self.barra.set)

        #self.lista.bind('<Double-1>', self.altera_itens_orc)
        #self.lista.bind('<Return>', self.altera_itens_orc)
        self.lista.bind('<Delete>', self.deletaItem)


Application()