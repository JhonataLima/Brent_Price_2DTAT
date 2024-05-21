#Importando bibliotecas necessárias
import pandas as pd
import numpy as np
import datetime
import yfinance as yf

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from datetime import date

import streamlit as st

import joblib

import warnings
warnings.filterwarnings('ignore')




# Carregar o modelo treinado
with open('model.pkl', 'rb') as file:
    model= joblib.load(file)

# Carregando os dados
df = pd.read_csv('/mount/src/brent_price_2dtat/ipea.csv')


#Atualizando os dados
indice = "BZ=F"

inicio = (pd.to_datetime(df['Data'].tail(1).values[0]) + pd.Timedelta(days=1))
data_ref = date.today()
final = data_ref.isoformat() 

dia_util= data_ref.weekday() <= 5

minimo= df['Preço'].min()
media = df['Preço'].mean()
maximo= df['Preço'].max()

# Função para filtrar o DataFrame por ano
def filter_year(df, year):
    # Certifique-se de que a coluna 'Data' está no formato correto de data e hora
    df['Data'] = pd.to_datetime(df['Data'])

    # Filtre o DataFrame para apenas o ano especificado
    df_filtered = df[df['Data'].dt.year == year]

    return df_filtered


# Montando Aplicação
st.title('PREÇO DO PETRÓLEO BRENT')
st.write('O PREÇO DO PETROLEO BRENT É UM DOS PRINCIPAIS INDICADORES DO MERCADO DE PETRÓLEO')


tab0, tab1, tab2= st.tabs(['GERAL', 'ANÁLISE|INSIGHTS', 'PREVISÃO'])

with tab0:
    st.write('### O QUE É O PETRÓLEO BRENT?')
    st.write('''O barril de petróleo do tipo Brent é uma referência global para o preço do petróleo bruto,
                 negociado principalmente na Europa e alguns outros mercados. 
        \n \nEle é extraído de campos localizados no Mar do Norte, próximo à Noruega e Dinamarca, 
                e possui características específicas, como densidade média e menor teor de enxofre.
        \n \n Seu preço é influenciado por diversos fatores, como acordos políticos, desastres naturais, 
             oferta e demanda global, flutuações de câmbio entre outros.''')

    # Gráfico
    fig = make_subplots(rows=1, cols=1)
    fig.add_trace(go.Scatter(x=df['Data'], y=df['Preço'], mode='lines', name='Preço do Petróleo Brent'), row=1, col=1)
    fig.update_layout(title='Histórico Preço do Petróleo Brent', xaxis_title='Data', yaxis_title='Preço')
    fig.update_xaxes(rangeslider_visible=True)
    st.plotly_chart(fig)

    col1, col2, col3 = st.columns(3)
    col1.metric('Preço Mínimo', f'{minimo:.2f}')
    col2.metric('Preço Médio', f'{media:.2f}')   
    col3.metric('Preço Máximo', f'{maximo:.2f}')

    st.write('\n \n')
    st.write('''Com base nesse grafico, podemos observar momentos de oscilação no preço.
              Os momentos de alta de 2014 e 2022 foram motivados  pela Primavera Árabe e saída da pandemia/invasão
              da Ucrânia. Enquanto 2014 a 2016 e início de 2020 foram observados nos períodos de superprodução e 
             início de pandemia. \n \nAbriremos os ultimos 4 anos nos Insights. ''')


with tab1:
    st.write('#### ANALISE HISTÓRICA DA SERIE')
    st.write('ANALISANDO PERIODOS DE GRANDES OSCILAÇÕES')
    st.write('\n \n')
    st.write('##### 2023')

    df_2023 = filter_year(df, 2023)
   

    # Gráfico
    fig = make_subplots(rows=1, cols=1)
    fig.add_trace(go.Scatter(x=df_2023['Data'], y=df_2023['Preço'], mode='lines', name='Preço do Petróleo Brent'), row=1, col=1)
    fig.update_layout(xaxis_title='Data', yaxis_title='Preço')
    fig.update_xaxes(rangeslider_visible=True)
    st.plotly_chart(fig)

    st.write(''' Em 2023, o preço do petróleo Brent começou o ano em alta devido ao aumento da demanda global e a retomada da economia mundial.
             Com a prolongação do conflito entre Rússia Ucrânia, os preços caíram e se estabilizaram, mas no final de 2023, uma nova alta 
             foi observada devido ao início de um conflito armado no Oriente Médio com a invasão do Hamas a Israel.
            ''')
    
    col1, col2, col3 = st.columns(3)
    col1.metric('Preço Mínimo', f'{df_2023["Preço"].min():.2f}', f'{minimo:.2f}')
    col2.metric('Preço Médio', f'{df_2023["Preço"].mean():.2f}', f'{media:.2f}')   
    col3.metric('Preço Máximo', f'{df_2023["Preço"].max():.2f}', f'{maximo:.2f}', delta_color='inverse')

    st.write('\n \n')
    st.write('\n \n')
    st.write('##### 2022')

    df_2022 = filter_year(df, 2022)

    # Gráfico
    fig = make_subplots(rows=1, cols=1)
    fig.add_trace(go.Scatter(x=df_2022['Data'], y=df_2022['Preço'], mode='lines', name='Preço do Petróleo Brent'), row=1, col=1)
    fig.update_layout(xaxis_title='Data', yaxis_title='Preço')
    fig.update_xaxes(rangeslider_visible=True)
    st.plotly_chart(fig)

    st.write('''
             O aumento dos preços do petróleo no início de 2022 está fortemente ligado à invasão da Ucrânia pela 
             Rússia em fevereiro desse ano. Embora os preços do petróleo já estivessem subindo, 
             o pico de 2022 ultrapassou a tendência esperada devido à instabilidade global provocada por este conflito. 
            \n \nAlém do petróleo, outras commodities energéticas foram impactadas, 
             incluindo o gás natural, devido à possibilidade de fechamento de dutos para a Europa. 
             Este cenário instável levou os preços do petróleo a US$ 127,98.
                ''')
    col1, col2, col3 = st.columns(3)
    col1.metric('Preço Mínimo', f'{df_2022["Preço"].min():.2f}', f'{minimo:.2f}')
    col2.metric('Preço Médio', f'{df_2022["Preço"].mean():.2f}', f'{media:.2f}')   
    col3.metric('Preço Máximo', f'{df_2022["Preço"].max():.2f}', f'{maximo:.2f}', delta_color='off')

    st.write('\n \n')
    st.write('\n \n')
    st.write('##### 2021')

    df_2021 = filter_year(df, 2021)

    # Gráfico
    fig = make_subplots(rows=1, cols=1)
    fig.add_trace(go.Scatter(x=df_2021['Data'], y=df_2021['Preço'], mode='lines', name='Preço do Petróleo Brent'), row=1, col=1)
    fig.update_layout(xaxis_title='Data', yaxis_title='Preço')
    fig.update_xaxes(rangeslider_visible=True)
    st.plotly_chart(fig)

    st.write('''
             Em 2021, a pandemia global manteve os preços do petróleo nos níveis mais baixos desde 2004. 
             No entanto, no segundo semestre, a gradual retomada das atividades industriais, de transporte e consumo levou
              a uma leve recuperação dos preços devido ao aumento da demanda.
              \n \nA OPEP+ também anunciou cortes na produção em meados de 2020, o que influenciou os preços com o 
             aumento das demandas em 2021. Teve o corte em 2021 assim como havia tido em
              2016 onde tbm foi possível observar a queda do preço.

                ''')
    col1, col2, col3 = st.columns(3)
    col1.metric('Preço Mínimo', f'{df_2021["Preço"].min():.2f}', f'{minimo:.2f}')
    col2.metric('Preço Médio', f'{df_2021["Preço"].mean():.2f}', f'{media:.2f}')   
    col3.metric('Preço Máximo', f'{df_2021["Preço"].max():.2f}', f'{maximo:.2f}', delta_color='inverse')

    st.write('\n \n')
    st.write('\n \n')

    st.write('\n \n')
    st.write('\n \n')
    st.write('##### 2020')

    df_2020 = filter_year(df, 2020)

    # Gráfico
    fig = make_subplots(rows=1, cols=1)
    fig.add_trace(go.Scatter(x=df_2020['Data'], y=df_2020['Preço'], mode='lines', name='Preço do Petróleo Brent'), row=1, col=1)
    fig.update_layout(xaxis_title='Data', yaxis_title='Preço')
    fig.update_xaxes(rangeslider_visible=True)
    st.plotly_chart(fig)

    st.write(''' No final de 2019, a pandemia trouxe mudanças drásticas à dinâmica mundial. Lockdowns, 
             fechamentos de aeroportos, turismo e eventos reduziram drasticamente a demanda por combustíveis, 
             causando uma queda acentuada nos preços do petróleo em abril de 2020. A falta de vacina e medidas 
             restritivas estagnaram muitos setores, com atividades não essenciais sendo realizadas remotamente 
             e o abastecimento reduzido. Com veículos parados e a diminuição do comércio internacional, 
             o valor do petróleo atingiu seu ponto mais baixo. Os preços começaram a subir novamente com a
              flexibilização das restrições, uma tendência observada globalmente a partir de meados de 2020.
            ''')
    col1, col2, col3 = st.columns(3)
    col1.metric('Preço Mínimo', f'{df_2020["Preço"].min():.2f}', f'{minimo:.2f}', delta_color='off')
    col2.metric('Preço Médio', f'{df_2020["Preço"].mean():.2f}', f'{media:.2f}', delta_color='inverse')   
    col3.metric('Preço Máximo', f'{df_2020["Preço"].max():.2f}', f'{maximo:.2f}', delta_color='inverse')


with tab2:
    st.write('Aqui faremos a previsão para o preço do petróleo Brent.')
    st.write('''O modelo de previsão selecionado é o GBR (Gradient Boosting Regressor) 
             que é atualizado diariamente com os dados mais recentes.''')

    numero = st.number_input('Quantos dias deseja prever', min_value=1, max_value=3, value=1, step=1)
    if dia_util == True:

        # Dados Faltantes a base
        up_df = yf.download(indice, inicio, final)
        up_df['Data'] = pd.to_datetime(df['Data'], format="%Y-%m-%d")
        
        # Verifique se os dados foram baixados corretamente
        if up_df.empty:
            warnings.filterwarnings('ignore')

        # Ajustando a base
        up_df['ds']= up_df.index.astype(str)
        up_df= up_df[['ds', 'Close']]
        up_df.rename(columns= {'Close' : 'Preço'}, inplace=True)
        up_df.rename(columns= {'ds' : 'Data'}, inplace=True)

        # Atualizando a base
        df = pd.concat([df, up_df], ignore_index=True)


        if st.button('Prever'):
            #Prevendo os proximos dias
            X = df[['Preço']].values

            last_known_data = X[-6].reshape(1, -6)
            next_week_predictions = []

            for _ in range(numero):  # para cada dia da próxima semana
                    next_day_pred = model.predict(last_known_data)[0]
                    next_week_predictions.append(next_day_pred)
                    last_known_data = np.roll(last_known_data, -1)
                    last_known_data[0, -1] = next_day_pred

            # As datas correspondentes à próxima semana
            next_week_dates = pd.date_range(df['Data'].iloc[-1], periods=(numero + 1))[1:]

            # Selecionar os dados da semana atual (últimos x dias do dataset)
            current_week_dates = df['Data'].iloc[-numero:]
            current_week_prices = df['Preço'].iloc[-numero:]

                # Criando um DataFrame com as previsões
            df_previsoes = pd.DataFrame({'Data': next_week_dates, 'Previsão': next_week_predictions})
            st.dataframe(df_previsoes)

    else:
        st.warning("Os valores são atualizados apenas em dias úteis! \n\nVolte na Segunda.")


# exportando a base atualizada
df.to_csv('/mount/src/brent_price_2dtat/ipea.csv', index=False)
