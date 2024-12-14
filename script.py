import streamlit as st
import pandas as pd 
import time
import matplotlib.pyplot as plt
import plotly.graph_objects as go


    
st.logo(
    image="AccessEye.png",
    size="large"
)

st.title("Uploader un fichier d'enedis en format CSV")
uploaded_file = st.file_uploader("Choisisez un fichier dans votre repertoir !" ,  type=["csv"] )


if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, sep=";")
    df = df[df['Unité'] == "W"]
    # Prétraitement des données
    df['Horodate'] = pd.to_datetime(df['Horodate'])
    df.set_index('Horodate', inplace=True)
    columns_to_drop = ['Date de début', 'Date de fin', 'Nature', 'Pas',
                       'Indice de vraisemblance', 'Etat complémentaire',
                       'Grandeur métier', 'Identifiant PRM',"Grandeur physique","Etape métier" , "Unité"]
    df.drop(columns_to_drop, axis=1, inplace=True)



    df['Valeur'] = df['Valeur'].astype(int) / 1000

    df_resampled = df.resample('h').sum()
    

    st.sidebar.header("Sélectionnez une plage de temps")
    min_date = df_resampled.index.min()
    max_date = df_resampled.index.max()
    

    start_date = st.sidebar.date_input("Date de début", min_date ,format="DD/MM/YYYY")
    start_time = st.sidebar.time_input("Heure de début", value=pd.Timestamp(min_date).time())
    end_date = st.sidebar.date_input("Date de fin", max_date,format="DD/MM/YYYY")
    end_time = st.sidebar.time_input("Heure de fin", value=pd.Timestamp(max_date).time())


    start_datetime = pd.Timestamp.combine(start_date, start_time)
    end_datetime = pd.Timestamp.combine(end_date, end_time)


    filtered_df = df_resampled.loc[start_datetime:end_datetime]


    if not filtered_df.empty:       
        
        st.write(f"Affichage des données entre {start_datetime} et {end_datetime}")
        
        
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=filtered_df.index,
            y=filtered_df['Valeur'],
            mode='lines',
            name='Valeur',
            line=dict(color='#95c24e', width=3)
        ))

        fig.update_layout(
            title="Valeur sur la période sélectionnée",
            xaxis_title="Horodate",
            yaxis_title="Valeur",
            template="plotly_dark"
        )


        st.plotly_chart(fig)

        

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=filtered_df.index,
            y=filtered_df['Valeur'],
            mode='lines',
            name='Valeur',
            line=dict(color='#95c24e', width=3)
        ))

        fig.update_layout(
            title="Valeur sur la période sélectionnée",
            xaxis_title="Horodate",
            yaxis_title="Valeur",
            template="plotly_dark"
        )


        fig_scatter = go.Figure()

        fig_scatter.add_trace(go.Scatter(
            x=filtered_df.index,
            y=filtered_df['Valeur'],
            mode='markers',
            name='Valeur',
            marker=dict(color='#95c24e', size=5)
        ))

        fig_scatter.update_layout(
            title="Diagramme de dispersion des valeurs",
            xaxis_title="Horodate",
            yaxis_title="Valeur",
            template="plotly_dark"
        )

        st.plotly_chart(fig_scatter)
        
        st.dataframe(df, use_container_width=True)
        st.dataframe(df['Valeur'].describe(), use_container_width=True)
        
    else:
        st.warning("Aucune donnée disponible pour la plage sélectionnée.")