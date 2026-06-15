# Predictive Maintenance — Machine Learning Web App

Prediksi kegagalan mesin menggunakan **Random Forest Classifier** berbasis dataset AI4I 2020.

## Struktur Folder

```
web-app/
├── index.html          ← Frontend (UI)
├── vercel.json         ← Konfigurasi Vercel deployment
├── .gitignore
├── README.md
└── api/
    ├── predict.py      ← Backend Flask API
    ├── requirements.txt
    ├── model_rf.pkl    ← ⚠️ COPY dari hasil Colab
    └── scaler.pkl      ← ⚠️ COPY dari hasil Colab
```

## Langkah Deployment

### 1. Siapkan File Model
Copy file berikut dari hasil Google Colab ke folder `api/`:
- `model_rf.pkl`
- `scaler.pkl`

### 2. Test Lokal (Opsional tapi Disarankan)
```bash
# Install dependencies
pip install -r api/requirements.txt

# Jalankan Flask
python api/predict.py

# Buka index.html di browser
# API berjalan di http://localhost:5000
```

### 3. Upload ke GitHub
```bash
git init
git add .
git commit -m "first commit: predictive maintenance ML app"
git branch -M main
git remote add origin https://github.com/USERNAME/REPO-NAME.git
git push -u origin main
```

### 4. Deploy ke Vercel
1. Buka https://vercel.com → Login dengan GitHub
2. Klik **"Add New Project"**
3. Import repository yang sudah diupload
4. Klik **Deploy** — Vercel otomatis baca `vercel.json`
5. Setelah deploy selesai, salin URL Vercel (contoh: `https://nama-app.vercel.app`)

### 5. Update URL API di Frontend
Buka `index.html`, cari baris:
```javascript
const API_URL = 'http://localhost:5000';
```
Ganti dengan URL Vercel kamu:
```javascript
const API_URL = 'https://nama-app.vercel.app';
```
Lalu commit dan push lagi → Vercel otomatis redeploy.

## API Endpoint

### POST `/api/predict`
**Request body:**
```json
{
  "type": "M",
  "air_temperature": 298.1,
  "process_temperature": 308.6,
  "rotational_speed": 1551,
  "torque": 42.8,
  "tool_wear": 108
}
```

**Response:**
```json
{
  "success": true,
  "prediction": 0,
  "label": "NORMAL",
  "probability_normal": 94.5,
  "probability_failure": 5.5
}
```

### GET `/api/health`
Cek apakah API berjalan.
