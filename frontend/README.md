# 🎯 Frontend - Product Analyzer UI

Modern React/Next.js frontend for the AI Dropshipping Agent platform.

## Features

✨ **Beautiful UI**
- Modern gradient design
- Responsive (mobile/tablet/desktop)
- Real-time form validation
- Smooth animations

📊 **Interactive Analysis**
- Real-time product analysis
- Profit breakdown visualization
- Success probability display
- Market intelligence dashboard
- Key factors & warnings

💰 **Complete Profit Breakdown**
- Selling price
- Product cost
- Platform fees (Shopify, Amazon, Etsy, TikTok, eBay)
- Payment processing fees
- Shipping costs
- Ad costs
- Return reserves

🎨 **Components**
- `AnalysisForm` - Product input form
- `ResultsDisplay` - Analysis results
- `RecommendationBadge` - Success score
- `ProfitBreakdownChart` - Visual breakdown
- `FactorsList` - Strengths & warnings

## Quick Start

### Installation

```bash
cd frontend
npm install
```

### Development

```bash
npm run dev
```

Visit `http://localhost:3000`

### Production Build

```bash
npm run build
npm start
```

## Configuration

### Environment Variables

Create `.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_API_KEY=test-key-123
```

For production:

```env
NEXT_PUBLIC_API_URL=https://api.yourdomain.com
NEXT_PUBLIC_API_KEY=your-real-api-key
```

## Backend Requirements

The frontend expects a running backend at `http://localhost:8000` with:

### Endpoint: `POST /products/analyze`

**Request:**
```json
{
  "selling_price": 39.99,
  "product_cost": 14.00,
  "shipping_from_supplier": 3.50,
  "shipping_to_customer": 0.00,
  "shipping_days": 7,
  "seller_count": 45,
  "review_count": 230,
  "platform": "shopify",
  "ad_cost_percent": 20.0
}
```

**Response:**
```json
{
  "success": true,
  "analysis": {
    "summary": { ... },
    "profit_analysis": { ... },
    "market_intelligence": { ... },
    "success_analysis": { ... }
  }
}
```

## Project Structure

```
frontend/
├── pages/
│   ├── _app.tsx           # App wrapper
│   └── index.tsx          # Main page
├── components/
│   ├── AnalysisForm.tsx   # Product input form
│   ├── ResultsDisplay.tsx # Analysis results
│   ├── RecommendationBadge.tsx
│   ├── ProfitBreakdownChart.tsx
│   └── FactorsList.tsx
├── lib/
│   ├── api.ts             # API client
│   └── types.ts           # TypeScript types
├── styles/
│   └── globals.css        # Global styles + Tailwind
├── package.json
├── tsconfig.json
├── next.config.js
├── tailwind.config.js
└── postcss.config.js
```

## Technology Stack

- **Framework:** Next.js 14
- **Language:** TypeScript
- **Styling:** Tailwind CSS
- **Charts:** Recharts
- **HTTP Client:** Axios
- **Build Tool:** Webpack (via Next.js)

## Features Breakdown

### 1. Product Analysis Form

Allows users to enter:
- Selling price & product cost
- Shipping (from supplier, to customer)
- Ad cost percentage
- Platform selection
- Market data (seller count, reviews)

### 2. Real-Time Analysis

Displays:
- Success probability (0-100%)
- NET profit (not fake margins)
- Profit breakdown pie chart
- Key strengths
- Potential warnings
- Clear recommendation

### 3. Market Intelligence

Shows:
- Competition level (VERY LOW → VERY HIGH)
- Number of sellers
- Demand trend (RISING/STABLE/FALLING)
- Shipping time impact
- Market validation (reviews)

### 4. Visual Feedback

- Color-coded recommendations (🟢 BUY, 🟡 CONSIDER, 🔴 AVOID)
- Progress bar for success probability
- Profit breakdown pie chart
- Responsive cards for key metrics

## Deployment

### Vercel (Recommended)

```bash
npm install -g vercel
vercel
```

Set environment variables in Vercel dashboard:
- `NEXT_PUBLIC_API_URL`
- `NEXT_PUBLIC_API_KEY`

### Docker

```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npm", "start"]
```

```bash
docker build -t dropshipping-frontend .
docker run -p 3000:3000 -e NEXT_PUBLIC_API_URL=https://api.yourdomain.com dropshipping-frontend
```

### Traditional Hosting

```bash
npm run build
npm start
```

Then run with PM2 or systemd.

## Troubleshooting

### API Connection Error

**Error:** "Failed to analyze product. Make sure the backend is running!"

**Solution:**
1. Check backend is running: `uvicorn app.main:app --reload`
2. Verify API URL in `.env.local`
3. Check CORS is enabled in backend

### TypeScript Errors

```bash
npm install --save-dev @types/react @types/node typescript
```

### Styling Not Loading

```bash
npm install -D tailwindcss postcss autoprefixer
npm run dev
```

## Performance

- ⚡ < 100ms API response time
- 📦 Lightweight bundle (~50KB gzipped)
- 🎨 Smooth animations (60fps)
- 📱 Mobile optimized
- 🔍 SEO friendly

## Future Enhancements

- [ ] CSV batch upload
- [ ] Historical product tracking
- [ ] Platform comparison charts
- [ ] User authentication
- [ ] Saved analysis history
- [ ] Email alerts for hot products
- [ ] Dark mode
- [ ] Multi-language support

## License

MIT

## Support

Need help? Check the backend docs at `../README.md`

---

**Built with ❤️ for dropshippers**
