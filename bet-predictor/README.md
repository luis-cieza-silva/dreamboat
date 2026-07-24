# bet-predictor

MVP de backtesting de una estrategia de apuestas simple: apostar a que un
equipo dominante (alto % de partidos ganados) gane cada partido que juega,
usando datos y cuotas históricas reales de La Liga.

## Idea

1. Algunos equipos grandes ganan un porcentaje muy alto de sus partidos en
   una temporada (Barcelona, Real Madrid, etc.).
2. Se simula apostar un monto fijo a que ese equipo gana, en cada uno de sus
   partidos, usando las cuotas reales del mercado en ese momento.
3. Se genera un cronograma (fecha por fecha) de apuestas, con el resultado de
   cada una y la evolución del profit acumulado.
4. Si el % de victorias real es suficientemente alto respecto a lo que
   implican las cuotas, la estrategia debería dar un ROI positivo a largo
   plazo.

## Datos

Se usan los CSV históricos gratuitos de [football-data.co.uk](https://www.football-data.co.uk/spainm.php)
para La Liga (código `SP1`), que incluyen resultados y cuotas 1X2 de varias
casas de apuestas (se prioriza Bet365, con fallback a otras casas si falta).
Los CSV se descargan una vez y se cachean en `bet-predictor/data/` (ya
ignorado por git vía el `*.csv` del `.gitignore` del repo).

## Uso

```bash
uv run bet-predictor/main.py
```

Por defecto corre el backtest para Barcelona y Real Madrid, apostando 10
(soles/unidad configurable) por partido, en las temporadas 2014/15 a
2023/24.

Parámetros opcionales:

```bash
uv run bet-predictor/main.py \
  --teams Barcelona "Real Madrid" Atletico Madrid \
  --stake 10 \
  --seasons-start 2018 \
  --seasons-end 2023 \
  --output bet-predictor/data/mi_cronograma.csv
```

La configuración por defecto (equipos, temporadas, stake, prioridad de
columnas de cuotas) vive en [`config.py`](./config.py).

## Salida

- En consola: % de partidos ganados por temporada de cada equipo, y un
  resumen del backtest (apuestas, aciertos, capital apostado, profit, ROI%).
- En CSV (`data/schedule.csv` por defecto): el cronograma completo de
  apuestas simuladas, con fecha, rival, condición (local/visitante), cuota
  usada, resultado y profit acumulado — ordenado cronológicamente, tal como
  se habrían ido colocando las apuestas a lo largo de las temporadas.

## Limitaciones importantes (léelo antes de confiar en el ROI)

- **Esto es un backtest retrospectivo, no una predicción real.** La
  estrategia apuesta siempre al mismo equipo usando el resultado y la cuota
  *ya conocidos* de cada partido histórico. No estima de antemano si el
  equipo va a ganar la temporada que viene: eso requeriría calcular el % de
  victorias con datos *anteriores* al partido (p. ej. temporada previa) para
  evitar look-ahead bias. Es el siguiente paso natural si se quiere usar
  esto para apostar hacia adelante.
- El ROI depende mucho de las temporadas y del equipo elegido: puede ser
  positivo en unas ventanas de tiempo y negativo en otras (lesiones, cambios
  de entrenador, temporadas flojas, etc.).
- Las cuotas históricas usadas son de cierre/apertura según la casa
  disponible por temporada, no necesariamente la mejor cuota posible en el
  mercado en ese momento.
- No es asesoría financiera ni una recomendación de apuesta real; es una
  herramienta de análisis y exploración de datos.
