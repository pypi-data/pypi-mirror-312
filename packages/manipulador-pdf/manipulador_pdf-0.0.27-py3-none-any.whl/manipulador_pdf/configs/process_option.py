from .salva_relatorio import salva_relatorio
from ..functions.documentos_admissao import documentos_admissao
from datetime import datetime
import time



def process_option(option: int) -> None:
    """
    Processa a opção do usuário.
    """
    data = datetime.now().strftime("%d/%m/%Y")
    st = time.time()

    if option == 0:
        info_hub()
    elif option == 1:
        n_pags = documentos_admissao()
        values = [[data, 'Documentos de Admissão', n_pags, time.time()-st]]
    elif option == 2:
        n_pags = documentos_rescisao()
        values = [[data, 'Documentos de Rescisão', n_pags, time.time()-st]]
    elif option == 3:
        n_pags = boletos_bmp()
        values = [[data, 'Boletos BMP', n_pags, time.time()-st]]
    elif option == 4:
        n_pags = boletos_cobranca()
        values = [[data, 'Boletos de Cobrança', n_pags, time.time()-st]]
    elif option == 5:
        n_pags = fichas_de_registro()
        values = [[data, 'Fichas de Registro', n_pags, time.time()-st]]
    elif option == 6:
        n_pags = folha_rescisao_ferias()
        values = [[data, 'Folha de Pagamento, Férias e Rescisão', n_pags, time.time()-st]]
    elif option == 7:
        n_pags = guias_fgts()
        values = [[data, 'Guias FGTS', n_pags, time.time()-st]]
    elif option == 8:
        n_pags = listagem_conferencia()
        values = [[data, 'Listagem de Conferência', n_pags, time.time()-st]]
    elif option == 9:
        n_pags = recibos_pagamento()
        values = [[data, 'Recibos de Pagamento', n_pags, time.time()-st]]
    elif option == 10:
        n_pags = recibos_folk()
        values = [[data, 'Recibos FOLK', n_pags, time.time()-st]]
    elif option == 11:
        n_pags = rel_servicos_adm()
        values = [[data, 'Relatório de Serviços Administrativos', n_pags, time.time()-st]]
    elif option == 12:
        n_pags = resumo_geral_mes_periodo()
        values = [[data, 'Resumo Geral Mês/Período', n_pags, time.time()-st]]
    elif option == 31:
        n_pags = nfs_curitiba()
        values = [[data, 'NFs Curitiba', n_pags, time.time()-st]]
    elif option == 32:
        n_pags = nfs_fortaleza()
        values = [[data, 'NFs Fortaleza', n_pags, time.time()-st]]
    elif option == 33:
        n_pags = nfs_salvador()
        values = [[data, 'NFs Salvador', n_pags, time.time()-st]]
    elif option == 34:
        n_pags = nfs_sorocaba()
        values = [[data, 'NFs Sorocaba', n_pags, time.time()-st]]

    if option != 0:
        salva_relatorio(values)

