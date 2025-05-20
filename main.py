from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph, SimpleDocTemplate, Frame, BaseDocTemplate, KeepInFrame
from reportlab.lib.pagesizes import A4  # Define qual o formato da folha.
from reportlab.lib.enums import TA_RIGHT, TA_LEFT, TA_JUSTIFY # Defino a direção que o texto vai ficar
from reportlab.lib.units import mm, inch, cm
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

from datetime import datetime  # Defino o horario da criação do documento
from pathlib import Path
import os

lista_causas = list()
MESES_CONSULTA = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
                  'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
SETORES_SEGETI = [
    'BPO Fiscal', 'BPO Trabalhista', 'Compliance Fiscal', 'Consultoria Tributaria', 'BPO Contabil',
    'Diretoria', 'BPO Financeiro', 'Legalizçao', 'Logistica', 'Outsourcing', 'Recusos Humanos',
    'Tecnologia da Informação'
]
""" ---------------------------------------------------------------------------------------------------------------- """

def data_hora_certa():
    valor_data = datetime.now()
    data_certa = valor_data.strftime('%d/%m/%Y')
    return data_certa

class CriandoDocumentoPdf(BaseDocTemplate):
    PATH_ATUAL = os.path.dirname(os.path.abspath(__file__))  # Busca a pasta atual do app
    DOC_SAVE_PATH = Path(PATH_ATUAL, 'static', 'dinamico', 'proc_melhoria')
    PAPEL_TIMBRADO = os.path.join(PATH_ATUAL, 'static', 'img', 'papel_timbrado', 'segeti_consultoria.png')
    ESTILOS = getSampleStyleSheet()

    # FONT_GOTHAN = pdfmetrics.registerFont(TTFont('GOTHAN', f'{os.path.join(
    #     PATH_ATUAL, 'static', 'pacotes', 'fonts', 'GothamNarrow-Medium.ttf')}'))
    # print(FONT_GOTHAN)
    """ ------------------------------------------------------------------------------------------------------------ """

    def __init__(self, dados_para_formatacao):
        super().__init__(self, **dados_para_formatacao)
        self.dados_para_formatacao_obj = dados_para_formatacao

        self._nome_cliente = None
        self._acontecimento = None

        self._o_que = None
        self._por_que = None
        self._quem = None
        self._onde = None
        self._quando = None
        self._como = None
        self._quanto = None
        self._list_causa_raiz = None
        self._acao_corretiva = None

        self.nome_documento = None
        self.documento = None
        self.data_certa = None
        self.papel_tibrado = None
        self._qtd_dados_causa_raiz = None

        self.ESTILO_PERSONALIZADO_TITULO = None
        self.ESTILO_PERSONALIZADO_DATA_CRIACAO = None
        self.ESTILO_PERSONALIZADO_TEXT = None

        self.lista_elementos_doc = list()

    # metado que gera o documento com as class do módulo
    def gerandor_documento(self):
        print('Passo 1: Criando documento')
        self.nome_documento = 'Primiro Documento.pdf'
        self.documento = SimpleDocTemplate(rf'{self.DOC_SAVE_PATH}\{self.nome_documento}', pagesize=A4)

        self._nome_cliente = self.dados_para_formatacao_obj['Cliente:']
        self._acontecimento = self.dados_para_formatacao_obj['Acontecimento:']

        self._list_causa_raiz = self.dados_para_formatacao_obj['causa_raiz']

        self._o_que = self.dados_para_formatacao_obj['perguntas']['_o_que']
        self._por_que = self.dados_para_formatacao_obj['perguntas']['_por_que']
        self._quem = self.dados_para_formatacao_obj['perguntas']['_quem']
        self._onde = self.dados_para_formatacao_obj['perguntas']['_onde']
        self._quando = self.dados_para_formatacao_obj['perguntas']['_quando']
        self._como = self.dados_para_formatacao_obj['perguntas']['_como']
        self._quanto = self.dados_para_formatacao_obj['perguntas']['_quanto']
        self._acao_corretiva = self.dados_para_formatacao_obj['Ação corretiva Sugerida']

        self._qtd_dados_causa_raiz = self.dados_para_formatacao_obj['qtd_dados_causa_raiz']

    # metado para formatar o texto principal no documento.
    def formatacao_documento(self):
        print('Passo 2: Formatado documento')
        self.estilo_documento()

        titulo = Paragraph(
            f'<p><font size="16"></font><p> <b></b>',
            self.ESTILO_PERSONALIZADO_TITULO)
        self.lista_elementos_doc.append(titulo)

        self.documento.build(self.lista_elementos_doc, onFirstPage=self.adicionando_canvas)

    # metodo que adiciona imgagem, linhas, e textos em determinados lugares dentro do documento.
    def adicionando_canvas(self, canvas, doc):
        print('Passo 3: Adicionando Canvas')

        width, height = A4
        self.estilo_documento()

        # Insere o papel timbrado da segeti
        canvas.drawImage(self.PAPEL_TIMBRADO, 0, 0, width=599, height=855)

        frame_cliente = Frame(20, 735, 195 * mm, 10 * mm, showBoundary=False)
        frame_cliente.addFromList(
            [Paragraph(
                f'<font size=12>Cliente: </font> <b>{self._nome_cliente}</b>', self.ESTILO_PERSONALIZADO_TEXT)],
            canvas)

        frame_acontecimento = Frame(20, 685, 195 * mm, 20 * mm, showBoundary=False)
        frame_acontecimento.addFromList(
            [Paragraph(
                f'<font size=12>Acontecimento: </font> <b>{self._acontecimento}</b>',
                self.ESTILO_PERSONALIZADO_TEXT)],
            canvas)

        """ Data da criação """
        canvas.setFont('Times-Roman', 12)
        canvas.setFillColor('#462f5b')
        data_criacao = f'Criado em: {data_hora_certa()}'
        canvas.drawString(30, 800, data_criacao)  # x , y


        # --------------------------------------------------------------------------------------------------------------
        # variaveis para o box pergunta
        _borda_perguntas = True  # Ativa a borda do frame
        _tamanho_box_pergunda = -43  # O frame de perguntas, possui a borda invertida.

        eixo_o_que_Y = 675  # Eixo responsável pela posição Y do item "o que"
        eixo_por_que_Y = 655  # Eixo responsável pela posição Y do item "por que"
        eixo_quem_Y = 635  # Eixo responsável pela posição Y do item "quem"
        eixo_quando_Y = 615  # Eixo responsável pela posição Y do item "quando"
        eixo_onde_Y = 615  # Eixo responsável pela posição Y do item "onde"
        eixo_como_Y = 595  # Eixo responsável pela posição Y do item "como"
        eixo_quanto_Y = 585  # Eixo responsável pela posição Y do item "quanto"

        size_box_text_o_que = 10  # Tamanho Y do frame do item "o que"
        size_box_text_por_que = 10  # Tamanho Y do frame do item "por que"
        size_box_text_como = 10  # Tamanho Y do frame do item "como"

        # --------------------------------------------------------------------------------------------------------------
        __eixo_Y_titulo_causa_raiz = 500
        __eixo_Y_box_causa_raiz = 155

        eixo_X = 20  # Configura a posição na horizontal
        eixo_Y = 443  # eixo que comando a posição das peguntas de causa

        _acao_corretiva_X = 20
        _acao_corretiva_Y = 380

        _primeira_linha_X = 175
        _primeiro_linha_Y = 175

        _segunda_linha_X = 153
        _segunda_linha_Y = 153

        espaco_entre_textos = 50
        espaco_entre_linhas = 14
        espaco_acao_causas = 40

        # --------------------------------------------------------------------------------------------------------------
        # Tamanho das Linhas
        inicio_linha = 7
        final_linha = 202
        # --------------------------------------------------------------------------------------------------------------

        print('_o_que', len(self._o_que))
        print('_por_que', len(self._por_que))
        print('_como', len(self._como))

        # ______________________________________________________________________________________________________________
        # 1° condição - Pergunta "o que"
        # Condição para quando os caracteres ficarem acima de 70, ajustando todo o documento para se manter na folha.

        # Calculando condição 1
        if len(self._como) > 82 and len(self._o_que) > 82 and len(self._por_que) > 285:
            print('- - ' * 30)
            print('Condição 1')
            print('Condição - len(self._como) > 82 and len(self._o_que) > 82 and len(self._por_que) > 285: ',
                  len(self._como) > 82 and len(self._o_que) > 82 and len(self._por_que) > 285)

            _tamanho_box_pergunda = -58
            size_box_text_o_que = 20  # Tamanho Y do frame do item "o que"
            size_box_text_por_que = 30  # Tamanho Y do frame do item "por que"
            size_box_text_como = 20

            eixo_o_que_Y = 650
            eixo_por_que_Y = 593
            eixo_quem_Y = 593
            eixo_quando_Y = 576
            eixo_onde_Y = 576
            eixo_como_Y = 532
            eixo_quanto_Y = 545

            __eixo_Y_titulo_causa_raiz = 500
            __eixo_Y_box_causa_raiz = 155

            eixo_Y = 443

            _primeira_linha_X = 175
            _primeiro_linha_Y = 175

            _segunda_linha_X = 153
            _segunda_linha_Y = 153

            _acao_corretiva_Y = 380

        # Calculando condição 2
        elif len(self._como) > 82 and len(self._o_que) > 82 and len(self._por_que) > 195:
            print('- - ' * 30)
            print('Condição 2')
            print('Condição - len(self._como) > 82 and len(self._o_que) > 82 and len(self._por_que) > 195: ',
                  len(self._como) > 82 and len(self._o_que) > 82 and len(self._por_que) > 195)

            _tamanho_box_pergunda = -55
            size_box_text_o_que = 20  # Tamanho Y do frame do item "o que"
            size_box_text_por_que = 20  # Tamanho Y do frame do item "por que"
            size_box_text_como = 20

            eixo_o_que_Y = 650
            eixo_por_que_Y = 620
            eixo_quem_Y = 605
            eixo_quando_Y = 589
            eixo_onde_Y = 589
            eixo_como_Y = 545
            eixo_quanto_Y = 553

            __eixo_Y_titulo_causa_raiz = 500
            __eixo_Y_box_causa_raiz = 155

            eixo_Y = 443

            _primeira_linha_X = 175
            _primeiro_linha_Y = 175

            _segunda_linha_X = 153
            _segunda_linha_Y = 153

            _acao_corretiva_Y = 380

        # Calculando condição 3
        elif len(self._como) > 82 and len(self._o_que) > 82 and len(self._por_que) > 82:
            print('- - ' * 30)
            print('Condição 3')
            print('Calculando condição 1: Pergunta "_como> 82, "_o_que > 82 " e "_por_que > 82": ',
                  len(self._como) > 70 and len(self._o_que) > 70 and len(self._por_que) > 69)

            _tamanho_box_pergunda = -53
            size_box_text_como = 20

            size_box_text_por_que = 20
            size_box_text_o_que = 20

            eixo_o_que_Y = 650
            eixo_por_que_Y = 620
            eixo_quem_Y = 620
            eixo_quando_Y = 601
            eixo_onde_Y = 601
            eixo_como_Y = 558
            eixo_quanto_Y = 558

            __eixo_Y_titulo_causa_raiz = 500
            __eixo_Y_box_causa_raiz = 155

            eixo_Y = 443

            _primeira_linha_X = 175
            _primeiro_linha_Y = 175

            _segunda_linha_X = 153
            _segunda_linha_Y = 153

            _acao_corretiva_Y = 380

        # Calculando condição 4
        elif len(self._como) > 82 and len(self._o_que) > 82:
            print('- - ' * 30)
            print('Condição 4')
            print('Condição: len(self._como) > 82 and len(self._o_que) > 82: ',
                  len(self._como) > 70 and len(self._o_que) > 70)

            _borda_perguntas = True
            _tamanho_box_pergunda = -48
            size_box_text_como = 20

            size_box_text_o_que = 20

            eixo_o_que_Y = 650
            eixo_por_que_Y = 650
            eixo_quem_Y = 635
            eixo_quando_Y = 620
            eixo_onde_Y = 620
            eixo_como_Y = 575
            eixo_quanto_Y = 575

            __eixo_Y_titulo_causa_raiz = 500
            __eixo_Y_box_causa_raiz = 155

            eixo_Y = 443

            _primeira_linha_X = 175
            _primeiro_linha_Y = 175

            _segunda_linha_X = 153
            _segunda_linha_Y = 153

            _acao_corretiva_Y = 380

        # Calculando condição 5
        elif len(self._por_que) > 285 and len(self._como) > 82:
            print('- - ' * 30)
            print('Condição 5')
            print('Condição - len(self._por_que) > 285 and len(self._como) > 82: ',
                  len(self._por_que) > 285 and len(self._como) > 82)

            _tamanho_box_pergunda = -58
            size_box_text_o_que = 10  # Tamanho Y do frame do item "o que"
            size_box_text_por_que = 30  # Tamanho Y do frame do item "por que"
            size_box_text_como = 20

            eixo_por_que_Y = 603
            eixo_quem_Y = 603
            eixo_quando_Y = 585
            eixo_onde_Y = 585
            eixo_como_Y = 540
            eixo_quanto_Y = 545

            __eixo_Y_titulo_causa_raiz = 500
            __eixo_Y_box_causa_raiz = 155

            eixo_Y = 443

            _primeira_linha_X = 175
            _primeiro_linha_Y = 175

            _segunda_linha_X = 153
            _segunda_linha_Y = 153

            _acao_corretiva_Y = 380

        # Calculando condição 6
        elif len(self._por_que) > 195 and len(self._como) > 82:
            print('- - ' * 30)
            print('Condição 6')
            print('Condição - len(self._por_que) > 195 and len(self._como) > 82: ',
                  len(self._por_que) > 195 and len(self._como) > 82)
            _tamanho_box_pergunda = -53
            size_box_text_o_que = 10  # Tamanho Y do frame do item "o que"
            size_box_text_por_que = 30  # Tamanho Y do frame do item "por que"
            size_box_text_como = 20

            eixo_por_que_Y = 600
            eixo_quem_Y = 613
            eixo_quando_Y = 595
            eixo_onde_Y = 595
            eixo_como_Y = 550
            eixo_quanto_Y = 560

            __eixo_Y_titulo_causa_raiz = 500
            __eixo_Y_box_causa_raiz = 155

            eixo_Y = 443

            _primeira_linha_X = 175
            _primeiro_linha_Y = 175

            _segunda_linha_X = 153
            _segunda_linha_Y = 153

            _acao_corretiva_Y = 380

        # Calculando condição 7: como e por que
        elif len(self._por_que) > 82 and len(self._como) > 82:
            print('- - ' * 30)
            print('Condição 7')
            print('Condição - len(self._por_que) > 195 and len(self._como) > 82: ',
                  len(self._por_que) > 82 and len(self._como) > 82)

            _borda_perguntas = True
            _tamanho_box_pergunda = -50
            size_box_text_como = 20

            size_box_text_por_que = 20

            eixo_por_que_Y = 630
            eixo_quem_Y = 630
            eixo_quando_Y = 612
            eixo_onde_Y = 612
            eixo_como_Y = 565
            eixo_quanto_Y = 570

            __eixo_Y_titulo_causa_raiz = 500
            __eixo_Y_box_causa_raiz = 155

            eixo_Y = 443

            _primeira_linha_X = 175
            _primeiro_linha_Y = 175

            _segunda_linha_X = 153
            _segunda_linha_Y = 153

            _acao_corretiva_Y = 380

        # 'Calculando condição 8: Pergunta "por que > 285 e _o_que > 82"'
        elif len(self._por_que) > 285 and len(self._o_que) > 82:
            print('- - ' * 30)
            print('Condição 8')
            print('"_por_que > 285 e _o_que > 82": ', len(self._por_que) > 266 and len(self._o_que) > 82)

            _tamanho_box_pergunda = -55
            size_box_text_por_que = 30
            size_box_text_o_que = 20

            eixo_o_que_Y = 650
            eixo_por_que_Y = 593
            eixo_quem_Y = 590
            eixo_quando_Y = 573
            eixo_onde_Y = 573
            eixo_como_Y = 555
            eixo_quanto_Y = 550

            ___eixo_Y_titulo_causa_raiz = 500
            __eixo_Y_box_causa_raiz = 155

            eixo_Y = 443

            _primeira_linha_X = 175
            _primeiro_linha_Y = 175

            _segunda_linha_X = 153
            _segunda_linha_Y = 153

            _acao_corretiva_Y = 380

        # 'Calculando condição 9: Pergunta "_por_que > 178 e _o_que > 82"'
        elif len(self._por_que) > 195 and len(self._o_que) > 82:
            print('- - ' * 30)
            print('Condição 9')
            print("len(self._por_que) > 195 and len(self._o_que) > 82: ", len(self._por_que) > 195 and len(self._o_que) > 82)

            _tamanho_box_pergunda = -52
            size_box_text_por_que = 20
            size_box_text_o_que = 20

            eixo_o_que_Y = 650
            eixo_por_que_Y = 620
            eixo_quem_Y = 605
            eixo_quando_Y = 585
            eixo_onde_Y = 585
            eixo_como_Y = 565
            eixo_quanto_Y = 563

            __eixo_Y_titulo_causa_raiz = 525
            __eixo_Y_box_causa_raiz = 180

            eixo_Y = 465

            _primeira_linha_X = 185
            _primeiro_linha_Y = 185

            _segunda_linha_X = 160
            _segunda_linha_Y = 160

            _acao_corretiva_Y = 405

        # Calculando condição 10: pergundas "o que e por que"
        elif len(self._por_que) > 82 and len(self._o_que) > 82:
            print('- - ' * 30)
            print('Condição 10')
            print(' len(self._por_que) > 82 and len(self._o_que) > 82: ',
                  len(self._por_que) > 82 and len(self._o_que) > 82)

            _tamanho_box_pergunda = -50
            size_box_text_o_que = 20
            size_box_text_por_que = 20

            eixo_o_que_Y = 650
            eixo_por_que_Y = 620
            eixo_quem_Y = 618
            eixo_quando_Y = 600
            eixo_onde_Y = 600
            eixo_como_Y = 580
            eixo_quanto_Y = 570

            __eixo_Y_titulo_causa_raiz = 530
            __eixo_Y_box_causa_raiz = 185

            eixo_Y = 470

            _primeira_linha_X = 185
            _primeiro_linha_Y = 185

            _segunda_linha_X = 160
            _segunda_linha_Y = 160

            _acao_corretiva_Y = 405

        # Calculando condição 11: Pergunta "_por_que > 285"
        elif len(self._por_que) > 285:
            print('- - ' * 30)
            print('Condição 11')
            print('len(self._por_que) > 285: ', len(self._por_que) > 285)
            _tamanho_box_pergunda = -50
            size_box_text_por_que = 30
            size_box_text_o_que = 20

            eixo_o_que_Y = 650
            eixo_por_que_Y = 605
            eixo_quem_Y = 605
            eixo_quando_Y = 588
            eixo_onde_Y = 588
            eixo_como_Y = 570
            eixo_quanto_Y = 565

            __eixo_Y_titulo_causa_raiz = 500
            __eixo_Y_box_causa_raiz = 155

            eixo_Y = 443

            _primeira_linha_X = 175
            _primeiro_linha_Y = 175

            _segunda_linha_X = 153
            _segunda_linha_Y = 153

            _acao_corretiva_Y = 380

        # Calculando condição 12: Pergunta "o que > 139"
        elif len(self._por_que) > 195:
            print('- - ' * 30)
            print('Condição 12')
            print('len(self._por_que) > 195: ', len(self._por_que) > 195)
            _tamanho_box_pergunda = -51
            size_box_text_por_que = 20

            eixo_por_que_Y = 630
            eixo_quem_Y = 610
            eixo_quando_Y = 590
            eixo_onde_Y = 590
            eixo_como_Y = 570
            eixo_quanto_Y = 565

            __eixo_Y_titulo_causa_raiz = 500
            __eixo_Y_box_causa_raiz = 155

            eixo_Y = 443

            _primeira_linha_X = 175
            _primeiro_linha_Y = 175

            _segunda_linha_X = 153
            _segunda_linha_Y = 153

            _acao_corretiva_Y = 380

        # Calculando condição 13: Pergunta "como"
        elif len(self._como) > 82:
            print('- - ' * 30)
            print('Condição 13')
            print('len(self._como) > 82: ', len(self._como) > 82)

            _borda_perguntas = True
            _tamanho_box_pergunda = -48
            size_box_text_como = 20

            eixo_por_que_Y = 655
            eixo_quem_Y = 640
            eixo_quando_Y = 623
            eixo_onde_Y = 623
            eixo_como_Y = 575
            eixo_quanto_Y = 575

            __eixo_Y_titulo_causa_raiz = 500
            __eixo_Y_box_causa_raiz = 155

            eixo_Y = 443

            _primeira_linha_X = 175
            _primeiro_linha_Y = 175

            _segunda_linha_X = 153
            _segunda_linha_Y = 153

            _acao_corretiva_Y = 380

        # Calculando condição 14 Pergunta "o que"
        elif len(self._por_que) > 82:
            print('- - ' * 30)
            print('Condição 14')
            print('len(self._por_que) > 82: ',len(self._por_que) > 82)

            _tamanho_box_pergunda = -45
            size_box_text_por_que = 20

            eixo_por_que_Y = 630
            eixo_quem_Y = 630
            eixo_quando_Y = 610
            eixo_onde_Y = 610
            eixo_como_Y = 590
            eixo_quanto_Y = 580

            __eixo_Y_titulo_causa_raiz = 500
            __eixo_Y_box_causa_raiz = 155

            eixo_Y = 443

            _primeira_linha_X = 175
            _primeiro_linha_Y = 175

            _segunda_linha_X = 153
            _segunda_linha_Y = 153

            _acao_corretiva_Y = 380

        # Calculando a condição 15: perunta o que
        elif len(self._o_que) > 82:
            print('- - ' * 30)
            print('Condição 15')
            print('self._o_que > 82: ', len(self._o_que) > 82)

            _tamanho_box_pergunda = -48

            __eixo_Y_titulo_causa_raiz = 540  # Eixo responsável pela posição Y do título "causa raiz"
            __eixo_Y_box_causa_raiz = 195  # Eixo responsável pela posição Y do frame "causa raiz"
            size_box_text_o_que = 20  # Tamanho do frame que vai contem os dados da pegunta o que

            eixo_o_que_Y = 650  # Eixo responsável pela posição Y do item "o que"
            eixo_por_que_Y = 645  # Eixo responsável pela posição Y do item "por que"
            eixo_quem_Y = 625  # Eixo responsável pela posição Y do item "quem"
            eixo_quando_Y = 605  # Eixo responsável pela posição Y do item "quando"
            eixo_onde_Y = 605  # Eixo responsável pela posição Y do item "onde"
            eixo_como_Y = 585  # Eixo responsável pela posição Y do item "como"
            eixo_quanto_Y = 575  # Eixo responsável pela posição Y do item "quanto"

            __eixo_Y_titulo_causa_raiz = 500
            __eixo_Y_box_causa_raiz = 155

            eixo_Y = 443

            _primeira_linha_X = 175
            _primeiro_linha_Y = 175

            _segunda_linha_X = 153
            _segunda_linha_Y = 153

            _acao_corretiva_Y = 380

        # --------------------------------------------------------------------------------------------------------------

        # Frame Perguntas
        # 1 O QUE
        frame_o_que = Frame(20, eixo_o_que_Y, 195 * mm, size_box_text_o_que * mm, showBoundary=False)
        frame_o_que.addFromList([Paragraph(
            f'<font size=10>O que (What): </font><b>{self._o_que}</b>',
            self.ESTILO_PERSONALIZADO_TEXT)],
            canvas)

        # 2 Por que

        frame_por_que = Frame(20, eixo_por_que_Y, 195 * mm, size_box_text_por_que * mm, showBoundary=False)
        frame_por_que.addFromList([Paragraph(
            f'<font size=10>Por que (Why): </font><b>{self._por_que}</b>',
            self.ESTILO_PERSONALIZADO_TEXT)],
            canvas)

        # 3 QUEM
        frame_quem = Frame(20, eixo_quem_Y, 195 * mm, 10 * mm, showBoundary=False)
        frame_quem.addFromList([Paragraph(
            f'<font size=10>Quem (Who): </font><b>{self._quem}</b>',
            self.ESTILO_PERSONALIZADO_TEXT)], canvas)

        # 4 QUANDO
        frame_quando = Frame(20, eixo_quando_Y, 195 * mm, 10 * mm, showBoundary=False)
        frame_quando.addFromList([Paragraph(
            f'<font size=10>Quando (When): </font><b>{self._quando}</b>',
            self.ESTILO_PERSONALIZADO_TEXT)], canvas)

        # 5 ONDE
        frame_onde = Frame(380, eixo_onde_Y, 195 * mm, 10 * mm, showBoundary=False)
        frame_onde.addFromList([Paragraph(
            f'<font size=10>Onde (Where): </font><b>{self._onde}</b>',
            self.ESTILO_PERSONALIZADO_TEXT)], canvas)

        # 6 Como
        frame_como_ = Frame(20, eixo_como_Y, 195 * mm, size_box_text_como * mm, showBoundary=False)  # y, x
        frame_como_.addFromList([Paragraph(
            f'<font size=10>Como (How): </font><b>{self._como}</b>', self.ESTILO_PERSONALIZADO_TEXT)],
            canvas)

        """self._quanto"""
        canvas.setFont('Times-Roman', 12)
        canvas.setFillColor('#462f5b')
        canvas.drawString(390, eixo_quanto_Y, 'Quanto (How much): ')  # x , y

        canvas.setFont('Times-Bold', 12)
        canvas.setFillColor('#462f5b')
        canvas.drawString(495, eixo_quanto_Y, f'R$ {self._quanto}')  # x , y

        frame_perguntas = Frame(20, 702, 195 * mm, _tamanho_box_pergunda * mm, showBoundary=_borda_perguntas)
        frame_perguntas.addFromList([Paragraph("")], canvas)

        # --------------------------------------------------------------------------------------------------------------
        # Frames causa raiz
        """titulo causa raiz """
        canvas.setFont('Times-Roman', 14)
        canvas.setFillColor('#462f5b')
        canvas.drawString(30, __eixo_Y_titulo_causa_raiz, 'Cauza Raiz')  # x , y

        bordas_frame_causa_raiz = True
        if self._qtd_dados_causa_raiz < 7:
            # primeira linha
            # Inicio da linha, Posicao inicio, Fim da linha, Posição final
            canvas.line(7 * mm, _primeira_linha_X * mm, 202 * mm, _primeira_linha_X * mm)
            bordas_frame_causa_raiz = False

        # Frame principal da causa raiz
        frame_causa_raiz_ = Frame(20, __eixo_Y_box_causa_raiz, 195 * mm, 120 * mm,
                                  showBoundary=bordas_frame_causa_raiz)
        frame_causa_raiz_.addFromList([Paragraph(
            f'<font size=12></font><b>{''}</b>',
            self.ESTILO_PERSONALIZADO_TEXT)],
            canvas)

        # Frame para cada cauza que for selecionada
        for indice, item in enumerate(self._list_causa_raiz):
            frame_descricao_cauza_raiz = Frame(eixo_X, eixo_Y, 195 * mm, 20 * mm, showBoundary=False)
            frame_descricao_cauza_raiz.addFromList([Paragraph(
                f'<font size=12> {self._list_causa_raiz[indice]['grupo']} </font>: '
                f'<b>{self._list_causa_raiz[indice]['titulo_descricao']}</b> | '
                f'<b>{self._list_causa_raiz[indice]['descricao_causa']}</b>',
                self.ESTILO_PERSONALIZADO_TEXT)],
                canvas)
            eixo_Y = eixo_Y - espaco_entre_textos

            _segunda_linha_X = _segunda_linha_X - espaco_entre_linhas
            _segunda_linha_Y = _segunda_linha_Y - espaco_entre_linhas

            _acao_corretiva_Y = _acao_corretiva_Y - espaco_acao_causas
        # --------------------------------------------------------------------------------------------------------------
        # segunda linha
        # Inicio da linha, Posicao inicio, Fim da linha, Posição final
        if self._qtd_dados_causa_raiz == 7:
            inicio_linha = 0
            final_linha = 0

        canvas.line(inicio_linha * mm, _segunda_linha_X * mm, final_linha * mm, _segunda_linha_Y * mm)

        frame_acao_corretiva = Frame(_acao_corretiva_X, _acao_corretiva_Y, 195 * mm, 20 * mm, showBoundary=False)
        frame_acao_corretiva.addFromList([Paragraph(
            f'<font size=12>Ação corretiva Sugerida: </font> <b>{self._acao_corretiva}</b>',
            self.ESTILO_PERSONALIZADO_TEXT)],
            canvas)

    # metodos onde possui os estilos ao documento
    def estilo_documento(self):
        self.ESTILO_PERSONALIZADO_TITULO = ParagraphStyle(
            'estilo',
            parent=self.ESTILOS['Normal'],
            fontName='Times-Roman',
            fontSize=25,  # Define o tamanho da fonte
            leading=30,  # Define o espaçamento entre linhas
            textColor='#462f5b',
            alignment=TA_LEFT
        )

        self.ESTILO_PERSONALIZADO_DATA_CRIACAO = ParagraphStyle(
            'estilo',
            parent=self.ESTILOS['Normal'],
            fontName='Times-Roman',
            fontSize=14,  # Define o tamanho da fonte
            leading=16,  # Define o espaçamento entre linhas
            textColor='#462f5b',
            alignment=TA_RIGHT
        )

        self.ESTILO_PERSONALIZADO_TEXT = ParagraphStyle(
            'estilo',
            parent=self.ESTILOS['Normal'],
            fontName='Times-Roman',
            fontSize=12,  # Define o tamanho da fonte
            leading=14,  # Define o espaçamento entre linhas
            textColor='#462f5b',
            alignment=TA_JUSTIFY,
            spaceAfter=1,
        )


def identificacao_causa_raiz(index_lista_cauxa_raiz):
    lista_grupo_de_cauzas_raiza = [
        '- Falha de Processo',
        '- Falhas de Comunicação',
        '- Falhas Humanas',
        '- Sobrecarga de Trabalho',
        '- Falta de Ferramentas Adequadas',
        '- Problemas de Gestão',
        '- Falhas de Planejamento',
    ]

    descricao_cauza_raiz = [

        {'0-Documentação Incompleta': 'Informações importantes não foram registradas adequadamente, '
                                      'resultando em falhas operacionais.'},

        {'0-Processos Desatualizados': 'Procedimentos antigos ou inadequados que não refletem as '
                                       'mudanças nas práticas ou nos regulamentos.'},

        {
            '1-Falta de Alinhamento': 'Ocorre quando os responsáveis por um processo não estão cientes das mudanças ou não '
                                      'receberam instruções claras.'},

        {
            '1-Comunicação Ineficiente': 'Mensagens importantes foram mal interpretadas ou não transmitidas de forma clara.'},

        {'2-Esquecimento': 'O colaborador deixou de realizar uma tarefa crucial devido à sobrecarga de atividades ou '
                           'falta de atenção.'},

        {
            '2-Falta de Treinamento': 'O colaborador não recebeu o treinamento adequado para realizar a tarefa corretamente.'},

        {
            '2-Falta de Atenção': 'Pode ser causada por excesso de tarefas, distrações no ambiente de trabalho ou falta de '
                                  'clareza na execução da tarefa. Ocorre quando o colaborador não presta atenção ao realizar uma tarefa, '
                                  'levando a erros ou omissões.'},

        {
            '2-Excesso de Tarefas': 'O colaborador tem mais atividades do que pode lidar, o que resulta em erros ou atrasos'},

        {'2-Falta de Prioridade': 'Falha em definir claramente o que é mais urgente e importante.'},

        {
            '3-Excesso de Tarefas': 'O colaborador tem mais atividades do que pode lidar, o que resulta em erros ou atrasos.'},

        {'3-Falta de Prioridade': 'Falha em definir claramente o que é mais urgente e importante.'},

        {
            '4-Sistemas Ineficientes': 'Ferramentas ou softwares utilizados não são adequados para a complexidade ou volume '
                                       'do trabalho, causando atrasos e erros.'},

        {'4-Falta de Automatização': 'Processos manuais que poderiam ser automatizados estão contribuindo para erros '
                                     'humanos.'},

        {'5-Deficiência na Alocação de Recursos': 'Recursos humanos ou materiais mal distribuídos para a execução de '
                                                  'determinadas tarefas.'},

        {'5-Falta de Monitoramento e Controle': 'Falta de uma supervisão adequada para garantir que os processos estão '
                                                'sendo executados corretamente.'},

        {'6-Previsão Inadequada de Demandas': 'O volume de trabalho ou prazos não foi bem planejado, '
                                              'resultando em gargalos.'},

        {'6-Falta de Contingência': 'Não ter um plano de ação para quando ocorrem problemas ou imprevistos.'},
    ]
    valor_busca = descricao_cauza_raiz[index_lista_cauxa_raiz]

    codigo_grupo_motivo = [x.split('-')[0] for x in valor_busca.keys()]
    motivo_cauza_raiz = [x.split('-')[-1] for x in valor_busca.keys()]
    descricao_do_motivo = [x.split('-')[-1] for x in valor_busca.values()]

    dict_falhas_humana = {
        'grupo': lista_grupo_de_cauzas_raiza[int(codigo_grupo_motivo[0])],
        'titulo_descricao': motivo_cauza_raiz[0],
        'descricao_causa': descricao_do_motivo[0],
    }
    return dict_falhas_humana


""" ---------------------------------------------------------------------------------------------------------------- """
if __name__ == '__main__':

    _var_cliente = 'Python - PyCharm'
    _var_acontecimento = 'Viva com leveza'

    _var_o_que = ('A criatividade é a inteligência se divertindo, e quando você permite que ela flua livremente, grandes '
                  'ideias surgem e transformam o mundo ao seu redor de maneiras incríveis.')

    _var_por_que = ('Sob o céu bordado de estrelas, onde o tempo sussurra segredos antigos ao vento, a alma vagueia '
                    'entre memórias e esperanças, colhendo silêncios e sonhos. Cada passo é verso, cada suspiro, '
                    'canção. E no compasso do universo, o coração aprende que a beleza mora no instante que se deixa '
                    'viver com ternura.')

    _var_quem = 'Gasparsinho Camarada'
    _var_onde = SETORES_SEGETI[10]
    _var_quando = f'{MESES_CONSULTA[1]}/2022'
    _var_como = ('No silêncio da noite, onde os sonhos dançam com as estrelas, a alma encontra abrigo nas palavras '
                 'suaves do vento, e o tempo se curva diante da beleza do instante eterno.')
    _var_quanto = '999.999,99'


    dict_dados_perguntas = {
        '_o_que': _var_o_que,
        '_por_que': _var_por_que,
        '_quem': _var_quem,
        '_onde': _var_onde,
        '_quando': _var_quando,
        '_como': _var_como,
        '_quanto': _var_quanto,
    }

    _var_causa_raiz_falhas_processo = None # 1
    _var_causa_raiz_falhas_comunicacao = None # 3
    _var_causa_raiz_falhas_humana = None # 6
    _var_causa_raiz_sobrecarga_trabalho =  10
    _var_causa_raiz_falta_ferramentas_adequadas =  12
    _var_causa_raiz_problemas_gestao = None # 13
    _var_causa_raiz_falhas_planejameto = None # 16

    _var_acao_corretiva = 'Criado um fluxo de tarefas'

    """ -------------------------------------------------------------- """
    if not _var_causa_raiz_falhas_processo is None:
        lista_causas.append(identificacao_causa_raiz(_var_causa_raiz_falhas_processo))

    if not _var_causa_raiz_falhas_comunicacao is None:
        lista_causas.append(identificacao_causa_raiz(_var_causa_raiz_falhas_comunicacao))

    if not _var_causa_raiz_falhas_humana is None:
        lista_causas.append(identificacao_causa_raiz(_var_causa_raiz_falhas_humana))

    if not _var_causa_raiz_sobrecarga_trabalho is None:
        lista_causas.append(identificacao_causa_raiz(_var_causa_raiz_sobrecarga_trabalho))

    if not _var_causa_raiz_falta_ferramentas_adequadas is None:
        lista_causas.append(identificacao_causa_raiz(_var_causa_raiz_falta_ferramentas_adequadas))

    if not _var_causa_raiz_problemas_gestao is None:
        lista_causas.append(identificacao_causa_raiz(_var_causa_raiz_problemas_gestao))

    if not _var_causa_raiz_falhas_planejameto is None:
        lista_causas.append(identificacao_causa_raiz(_var_causa_raiz_falhas_planejameto))

    print(len(lista_causas))
    """ -------------------------------------------------------------- """

    dados_entrada_documento = {
        'Cliente:': _var_cliente,
        'Acontecimento:': _var_acontecimento,
        'perguntas': dict_dados_perguntas,
        'causa_raiz': lista_causas,
        'Ação corretiva Sugerida': _var_acao_corretiva,
        'qtd_dados_causa_raiz': len(lista_causas)
    }

    # for k, v in dados_entrada_documento.items():
    #     print('* * ' * 14)
    #     if k == 'Cauza Raiz':
    #         print(k)
    #         for valor in v:
    #             print(valor)
    #     else:
    #         print(k, v)

    iniciando_obj = CriandoDocumentoPdf(dados_entrada_documento)
    iniciando_obj.gerandor_documento()
    iniciando_obj.formatacao_documento()
