#Jerônimo

#Importação das funções do banco
from banco_componentes import limpa_componentes
from banco_triggers import limpa_triggers
from banco_horarios import limpa_horarios
from banco_ifttt import limpa_ifttt
from canais_raspberry import limpa_canais

#Limpeza do banco
limpa_componentes()
limpa_triggers()
limpa_horarios()
limpa_ifttt()
limpa_canais()
