import pandas as pd 

from fastapi import FastAPI

app = FastAPI()

def listaPalabrasDicFrec(listaPalabras):
    frecuenciaPalab = [listaPalabras.count(p) for p in listaPalabras]
    return dict(list(zip(listaPalabras, frecuenciaPalab)))


def ordenaDicFrec(dicFrec):
    aux = [(dicFrec[key], key) for key in dicFrec]
    aux.sort()
    aux.reverse()
    return aux



@app.get('/get_max_duration')
def get_max_duration(anio:int, platform:str, type:str): 
    data = pd.read_csv('https://raw.githubusercontent.com/NicoGit333/Prueba_PI01/main/df_data.csv')
    data.duration_int = pd.to_numeric(data.duration_int, errors = 'coerce')
    data.release_year = pd.to_numeric(data.release_year, errors = 'coerce')
    query1 = data[(data['release_year'] == anio) & (data['plataforma'] == platform) & (data['duration_type'] == type)]
    query1 = query1.sort_values('duration_int', ascending=False)
    res = query1.head(1)
    res = res.title.to_list()

    return 'La pelicula que mas duro fue: ', str(''.join(res))


@app.get('/get_count_platform')
def get_count_platform(platform:str):
    data = pd.read_csv('https://raw.githubusercontent.com/NicoGit333/Prueba_PI01/main/df_data.csv')
    query2 = data['plataforma'] == platform
    count_query2 = data[query2]['type'].value_counts()

    return {'Plataforma':platform,
            'Movies':str(count_query2[0]),
            'Shows':str(count_query2[1])
            }

@app.get('/get_actor')
def get_actor(platform:str, anio:int):
    data = data = pd.read_csv('https://raw.githubusercontent.com/NicoGit333/Prueba_PI01/main/df_data.csv')

    act = data[(data['plataforma'] == platform) & (data['release_year'] == anio)].cast.str.split(',')
    act = act.dropna()

    actores_año = []
    for actores in act: 
        for actor in actores:
            actor = actor.rstrip()
            actor = actor.lstrip()
            actores_año.append(actor)

    actor = listaPalabrasDicFrec(actores_año)
    actor = ordenaDicFrec(actor)

    return f'El actor que mas se repite en: {platform} en el año: {anio} es: {actor[0][1]} con un total de: {actor[0][0]} apariciones.'