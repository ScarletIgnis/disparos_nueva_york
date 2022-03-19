# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import pandas as pd
import streamlit as st
import pydeck as pdk
import plotly.express as px
import plotly.graph_objects as go
import base64

st.set_page_config(layout='wide') #aprovechar el ancho de la pantalla

st.markdown("<h1 style='tex-align: center; color:#FF2D00; '> Historico de disparos en New York 💥 🗽 </h1>",unsafe_allow_html =True) #poner el nombre del dash board

@st.cache(persist=True)
def load_data(url):
    df=pd.read_csv(url)
    df['OCCUR_DATE']=pd.to_datetime(df['OCCUR_DATE'])
    df['OCCUR_TIME']=pd.to_datetime(df['OCCUR_TIME'], format='%H:%M:%S')
    df['YEAR']=df['OCCUR_DATE'].dt.year
    df['HOUR']=df['OCCUR_TIME'].dt.hour
    df['YEARMONTH']=df['OCCUR_DATE'].dt.strftime('%Y%m')
    df.columns=df.columns.map(str.lower)

    return df

def get_table_download_link(df):
    csv = df.to_csv(index =False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="datos.csv">Descargar archivo csv</a>'
    return href



df=load_data('NYPD_Shooting_Incident_Data__Historic_ (1).csv')
#df['latitude']=df['latitude'].astype('float')
#df['longitude']=df['longitude'].astype('float')

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
c1,c2,c3,c4,c5=st.columns((1,1,1,1,1))

c1.markdown("<h3 style ='text-align: center; color:Gray;'>Top Sexo</h3>", unsafe_allow_html =True)

top_perp_name=df['perp_sex'].value_counts().index[0]

top_perp_num=(round(df['perp_sex'].value_counts()/df['perp_sex'].value_counts().sum(),2)*100)[0]

top_vic_name=df['vic_sex'].value_counts().index[0]

top_vic_num=(round(df['vic_sex'].value_counts()/df['vic_sex'].value_counts().sum(),2)*100)[0]

c1.text('Atacante: '+ str(top_perp_name)+'; '+str(top_perp_num)+'%')

c1.text('Victima: '+ str(top_vic_name)+'; '+str(top_vic_num)+'%')

#---------------------------------------------------------------
c2.markdown("<h3 style ='text-align: center; color:Gray;'>Top Raza</h3>", unsafe_allow_html =True)

top_perp_name=df['perp_race'].value_counts().index[0]

top_perp_num=(round(df['perp_race'].value_counts()/df['perp_race'].value_counts().sum(),2)*100)[0]

top_vic_name=df['vic_race'].value_counts().index[0]

top_vic_num=(round(df['vic_race'].value_counts()/df['vic_race'].value_counts().sum(),2)*100)[0]

c2.text('Atacante: '+ str(top_perp_name)+'; '+str(top_perp_num)+'%')

c2.text('Victima: '+ str(top_vic_name)+'; '+str(top_vic_num)+'%')
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
c3.markdown("<h3 style ='text-align: center; color:Gray;'>Top Edad</h3>", unsafe_allow_html =True)

top_perp_name=df['perp_age_group'].value_counts().index[0]

top_perp_num=(round(df['perp_age_group'].value_counts()/df['perp_age_group'].value_counts().sum(),2)*100)[0]

top_vic_name=df['vic_age_group'].value_counts().index[0]

top_vic_num=(round(df['vic_age_group'].value_counts()/df['vic_age_group'].value_counts().sum(),2)*100)[0]

c3.text('Atacante: '+ str(top_perp_name)+'; '+str(top_perp_num)+'%')

c3.text('Victima: '+ str(top_vic_name)+'; '+str(top_vic_num)+'%')

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
c4.markdown("<h3 style ='text-align: center; color:Gray;'>Top Barrio</h3>", unsafe_allow_html =True)

top_perp_name=df['boro'].value_counts().index[0]

top_perp_num=(round(df['boro'].value_counts()/df['boro'].value_counts().sum(),2)*100)[0]

c4.text('Nombre: '+ str(top_perp_name)+'; '+str(top_perp_num)+'%')

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
c5.markdown("<h3 style ='text-align: center; color:Gray;'>Top Hora</h3>", unsafe_allow_html =True)

top_perp_name=df['hour'].value_counts().index[0]

top_perp_num=(round(df['hour'].value_counts()/df['hour'].value_counts().sum(),2)*100)[0]

c5.text('Hora: '+ str(top_perp_name)+'; '+str(top_perp_num)+'%')
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

c1, c2 = st.columns((1,1)) #para que separe por partes iguales el dash board aunque si se pone como 1/3 algo ocupa un cuarto por ejemplo

c1.markdown("<h3 style='tex-align: center; color:#FF2D00; '> ¿Donde han ocurrido disparos en New York ? </h3>",unsafe_allow_html =True)
year=c1.slider('Año en el que ocurrió el suceso', df.year.min(), df.year.max())
c1.map(df[df['year']==year][['latitude','longitude']])

c2.markdown("<h3 style='tex-align: center; color:#FF2D00; '> ¿A que horas han ocurrido disparos en New York ? </h3>",unsafe_allow_html =True)
hour=c2.slider('Hora en la que ocurrió el suceso', int(df.hour.min()), int(df.hour.max()))
df2=df[df['hour']==hour]

c2.write(pdk.Deck(
         
    map_style= 'mapbox://styles/mapbox/light-v9',
         
    initial_view_state={
        'latitude': df['latitude'].mean(),
        'longitude': df['longitude'].mean(),
        'zoom': 9.5, #que tan cerca se ve
        'pitch':50}, #que tan ladeado estara
        
    layers=[pdk.Layer(
        'HexagonLayer',
        data=df[['latitude','longitude']],
        get_position=['longitude', 'latitude'],
        radius=100,
        extruded=True, #permite elevacion
        elevation_scale=4, #escala en la que estara elevado
        elevation_rage=[0,1000])]
        ))

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
st.markdown("<h3 style='tex-align: center; color:#FF2D00; '> ¿Como ha sido la evolución de disparos por barrio en New York ? </h3>",unsafe_allow_html =True)

df3 = df.groupby(['yearmonth','boro'])[['incident_key']].count().reset_index().rename(columns={'incident_key':'disparos'})

fig = px.line(df3, x='yearmonth',y='disparos', color ='boro', width =1400, height =450)


# Editar gráfica
fig.update_layout(
        title_x=0.5,
        plot_bgcolor='rgba(0,0,0,0)',
        template = 'simple_white',
        xaxis_title="<b>Año/mes<b>",
        yaxis_title='<b>Cantidad de incidentes<b>',
        legend_title_text='',
        
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=0.7))

st.plotly_chart(fig)

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
c4, c5, c6, c7= st.columns((1,1,1,1))

c4.markdown("<h3 style='tex-align: center; color:#FF2D00; '> ¿Que edad tienen los atacantes? </h3>",unsafe_allow_html =True)

df2=df.groupby(['perp_age_group'])[['incident_key']].count().reset_index().rename(columns={'incident_key':'disparos'})


df2['perp_age_group'] = df2['perp_age_group'].replace({'940':'N/A','224':'N/A',
                                                       '1020':'N/A','UNKNOWN':'N/A'})

df2['perp_age_group2'] = df2['perp_age_group'].replace({'<18':'1','18-24':'2','24-44':'3',
                                                       '45-64':'4', '65+':'5', 'N/A':'6'})

df2 = df2.sort_values('perp_age_group2')

fig = px.bar(df2, x='disparos', y='perp_age_group', orientation ='h', width=380, height =370)

#Editar grafica
fig.update_layout(plot_bgcolor='rgba(0,0,0,0)',
                  template = 'simple_white',
                  xaxis_title="<b>Atacante<b>",
                  yaxis_title='<b>Edades<b>')


c4.plotly_chart(fig)

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

c5.markdown("<h3 style='tex-align: center; color:#FF2D00; '> ¿Que edad tienen las victimas? </h3>",unsafe_allow_html =True)

df2=df.groupby(['vic_age_group'])[['incident_key']].count().reset_index().rename(columns={'incident_key':'disparos'})


df2['vic_age_group'] = df2['vic_age_group'].replace({'940':'N/A','224':'N/A',
                                                       '1020':'N/A','UNKNOWN':'N/A'})

df2['vic_age_group2'] = df2['vic_age_group'].replace({'<18':'1','18-24':'2','24-44':'3',
                                                       '45-64':'4', '65+':'5', 'N/A':'6'})

df2 = df2.sort_values('vic_age_group2')

fig = px.bar(df2, x='disparos', y='vic_age_group', orientation ='h', width=380, height =370)

#Editar grafica
fig.update_layout(plot_bgcolor='rgba(0,0,0,0)',
                  template = 'simple_white',
                  xaxis_title="<b>Victima<b>",
                  yaxis_title='<b>Edades<b>')


c5.plotly_chart(fig)

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

c6.markdown("<h3 style='tex-align: center; color:#FF2D00; '> ¿Cual es el sexo del atacante? </h3>",unsafe_allow_html =True)

df2=df.groupby(['perp_sex'])[['incident_key']].count().reset_index().sort_values('incident_key', ascending=False)

fig=px.pie(df2, values='incident_key', names='perp_sex', width=320,height=320)

# Editar gráfica
fig.update_layout(
        title_x=0.5,
        plot_bgcolor='rgba(0,0,0,0)',
        template = 'simple_white',
        legend_title_text='',
        
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.4,
            xanchor="center",
            x=0.5))

c6.plotly_chart(fig)


#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

c7.markdown("<h3 style='tex-align: center; color:#FF2D00; '> ¿Cual es el sexo de la  victima? </h3>",unsafe_allow_html =True)

df2=df.groupby(['vic_sex'])[['incident_key']].count().reset_index().sort_values('incident_key', ascending=False)

fig=px.pie(df2, values='incident_key', names='vic_sex', width=320,height=320)

# Editar gráfica
fig.update_layout(
        title_x=0.5,
        plot_bgcolor='rgba(0,0,0,0)',
        template = 'simple_white',
        legend_title_text='',
        
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.4,
            xanchor="center",
            x=0.5))
#definir por cada categoria los colores
c7.plotly_chart(fig)

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

st.markdown("<h3 style ='text-align: center; color:black;'>Evolución de disparos por año en las horas con más y menos sucesos</h3>", unsafe_allow_html =True)

df2 = df[df['hour'].isin([23,9])].groupby(['year','hour'])[['incident_key']].count().reset_index()

df2['hour']=df2['hour'].astype('category')

fig = px.bar(df2, x ='year', y ='incident_key', color ='hour', barmode='group', width =1150, height=450)

# Editar gráfica
fig.update_layout(
        title_x=0.5,
        plot_bgcolor='rgba(0,0,0,0)',
        template = 'simple_white',
        xaxis_title="<b>Año<b>",
        yaxis_title='<b>Cantidad de disparos<b>',
        legend_title_text='<b>Hora<b>')
        


st.plotly_chart(fig)

if st.checkbox('Obtener por fechas y barrio', False):
    df2=df.groupby(['occur_date','boro'])[['incident_key']].count().reset_index().rename(columns={'boro':'Barrio','occur_date':'Fecha', 'incident_key':'Disparos'})
    fig=go.Figure(data=[go.Table(
        
       header=dict(values=list(df2.columns),
       fill_color='darkred',
       line_color='darks lategray'),
       
       
       cells=dict(values=[df2.Fecha,df2.Barrio, df2.Disparos],
               fill_color='black',
               line_color='darks lategray'))])
    
    fig.update_layout(width=500, height=450)
    st.write(fig)

st.markdown(get_table_download_link(df2), unsafe_allow_html=True)

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------










