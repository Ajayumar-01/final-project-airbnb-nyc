# 🏠 NYC Airbnb Analysis - Final Project Winter 2025/2026

## 📊 Dataset Details
- **Source**: [Kaggle NYC Airbnb Open Data](https://www.kaggle.com/datasets/dgomonov/new-york-city-airbnb-open-data)
- **Size**: 48,895 listings (downloaded 2019 data)
- **Columns** (16 total): `id`, `name`, `host_id`, `host_name`, `neighbourhood_group`, `neighbourhood`, `latitude`, `longitude`, `room_type`, `price`, `minimum_nights`, `number_of_reviews`, `last_review`, `reviews_per_month`, `calculated_host_listings_count`, `availability_365`
- **Cleaning**: Removed price=0 + top 1% outliers → **48,410 clean listings**
- **File**: `data/AB_NYC_2019.csv` (7MB original)

## 🎯 Deliverables (All Requirements Met)
| Requirement | Location | Status |
|-------------|----------|--------|
| Jupyter notebook (10+ viz) | `notebooks/analysis.ipynb` | ✅ 11 questions |
| Dataset file | `data/AB_NYC_2019.csv` | ✅ Original + documented |
| Streamlit dashboard | Live: [UPDATE LINK] \| Code: `streamlit_app/app.py` | ✅ 11 interactive charts |
| PPT summary | `presentation/slides.pdf` | ⏳ Coming |

## 📈 Key Insights (from 11 analyses)
1. **Manhattan**: $155 median price (highest)
2. **Entire homes**: 3x private room prices
3. **Williamsburg**: 3,500+ listings (busiest area)
4. **No correlation**: reviews ↔ price
5. **Queens**: highest availability (140+ days/year)

## 🖥️ Run Instructions
```bash
# 1. Notebook (11 visualizations)
jupyter notebook notebooks/analysis.ipynb

# 2. Dashboard (interactive)
cd streamlit_app
pip install -r requirements.txt
streamlit run app.py
