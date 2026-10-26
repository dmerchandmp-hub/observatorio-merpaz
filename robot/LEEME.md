# Robot del Observatorio de Inversión MERPAZ

Programas que usa la tarea programada diaria (lunes a viernes, 07:30 hora Ecuador) para generar:

- `app_pwa.py`: la app del teléfono (`index.html`, `manifest.webmanifest`, `sw.js`) a partir del tablero.
- `extraer.js`: extrae del tablero los datos del día (`datos.json`).
- `reporte_pdf.py`: el reporte PDF de 4 páginas.
- `correo_html.py`: el cuerpo del correo diario.
- `tablero_pdf.js`: el PDF completo del tablero.

Solo usa datos públicos de mercado. Información referencial, no asesoría financiera.
