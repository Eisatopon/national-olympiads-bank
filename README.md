# Mathematical Olympiads Problem Bank 🌍

A comprehensive problem database from National Mathematical Olympiads worldwide (1985-2025).

## ✨ Features

### 🔍 Advanced Search
- **Keyword search** in problem statements
- Filters: Year, Country, Competition Type, Problem Number
- **Difficulty Filter**: Easy, Medium, Hard
- **Categories**: Algebra, Geometry, Combinatorics, Number Theory

### 💾 Save & Export
- **LocalStorage**: Automatic saving of your selection
- **PDF Export**: Export selected problems to PDF
- **Print**: Print with optimized formatting
- **QR Code**: Generate QR for sharing

### 📊 Statistics
- Total problems
- Number of countries
- Year range
- Selected problems count

### 🎨 Interface Features
- Responsive design (mobile-friendly)
- MathJax for mathematical formula rendering
- Country flags
- Dark mode ready (optional)

## 🚀 Installation

### Step 1: Create GitHub Repository

1. Create a new repository on GitHub:
   - Name: `olympiads-bank` (or your choice)
   - Public repository
   - Add README

### Step 2: Prepare JSON Files

Each year needs a JSON file with this structure:

```json
{
  "year": "2024",
  "problems": {
    "National Olympiads": {
      "China": [
        {
          "id": 1,
          "number": "1",
          "category": "Number Theory",
          "difficulty": "Medium",
          "statement": "Find all prime numbers $p$ such that..."
        }
      ],
      "Greece": [...],
      "Romania": [...]
    },
    "Selection Team Test": {
      "Iran": [...],
      "Brazil": [...]
    }
  }
}
```

**Required fields:**
- `id`: Unique number (integer)
- `number`: Problem number (string)
- `statement`: Problem statement (string with LaTeX)

**Optional fields:**
- `category`: "Algebra" | "Geometry" | "Combinatorics" | "Number Theory"
- `difficulty`: "Easy" | "Medium" | "Hard"

### Step 3: Upload to GitHub

```bash
# Files to upload
olympiads_1985.json
olympiads_1986.json
...
olympiads_2025.json
```

### Step 4: Update HTML

In the `olympiads_bank_enhanced.html` file, change `YOUR_USERNAME`:

```javascript
const DATA_URLS = {
    "2025": "https://raw.githubusercontent.com/YOUR_USERNAME/olympiads-bank/main/olympiads_2025.json",
    "2024": "https://raw.githubusercontent.com/YOUR_USERNAME/olympiads-bank/main/olympiads_2024.json",
    // ...
}
```

### Step 5: GitHub Pages (Optional)

1. Settings → Pages
2. Source: Deploy from branch
3. Branch: main, folder: / (root)
4. Save

Your site will be available at:
`https://YOUR_USERNAME.github.io/olympiads-bank/`

## 📝 Usage

### Search Problems

1. **Select year** (required)
2. Optional filters:
   - Keyword
   - Country
   - Category
   - Difficulty
   - Competition type
   - Problem number
3. Click "🔍 Search"

### Create Selection

1. Click "✅ Add" on each problem you want
2. Problems appear in "📝 My Selection"
3. **Automatic save** to localStorage

### Export

- **📄 Export PDF**: Export to PDF (without LaTeX rendering)
- **🖨️ Print**: Print (with LaTeX rendering)
- **📱 QR Code**: Generate QR for sharing
- **🗑️ Clear**: Clear selection

## 🎯 Tips for JSON Creation

### LaTeX Formatting

```javascript
// Inline math
"Find $x$ such that $x^2 = 4$"

// Display math
"Prove that:\n\n$$\\sum_{i=1}^{n} i = \\frac{n(n+1)}{2}$$"

// Multiple lines
"Given:\n\n$$a + b = c$$\n\n$$ab = 1$$"
```

### Difficulty Guidelines

- **Easy**: Problems for beginners (usually P1-P2)
- **Medium**: Moderate difficulty (P3-P4)
- **Hard**: Difficult problems (P5-P6, Selection Tests)

### Category Assignment

- **Algebra**: Inequalities, equations, polynomials
- **Geometry**: Triangles, circles, geometric properties
- **Combinatorics**: Counting, graphs, principles
- **Number Theory**: Primes, divisibility, modular arithmetic

## 🛠️ Customizations

### Add Countries

1. Add to `<select id="country">`:
```html
<option value="USA">USA</option>
```

2. Optional: Add flag to `.flags-banner`

### Add Categories

```html
<select id="category">
    <option value="Functional Equations">Functional Equations</option>
</select>
```

### Custom Styling

Change colors in CSS:

```css
.header {
    background: linear-gradient(135deg, #your-color-1, #your-color-2);
}
```

## 📱 Responsive Design

- Desktop: Full grid layout
- Tablet: 2-column layout
- Mobile: Single column, optimized buttons

## 🔧 Technical Details

### Libraries Used

- **MathJax 3**: For LaTeX rendering
- **jsPDF**: For PDF generation
- **QRCode.js**: For QR code generation

### Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

### LocalStorage Structure

```javascript
{
  "olympiadsSelection": [
    {
      "id": 1,
      "year": "2024",
      "country": "China",
      "type": "National Olympiads",
      "problem_number": "1",
      "content": "...",
      "category": "Algebra",
      "difficulty": "Medium"
    }
  ]
}
```

## 📊 Example JSON Structure

See `olympiads_2024_example.json` for a complete example.

## 🐛 Troubleshooting

### Loading Issues

1. **404 Error**: Check that the URL is correct
2. **CORS Error**: Use GitHub Pages or local server
3. **Math not rendering**: Wait a bit, MathJax is loading

### LocalStorage Issues

```javascript
// Clear cache
localStorage.clear();
location.reload();
```

## 🎓 Use Cases

- Preparation for competitions
- Creating exams
- Study by category/difficulty
- Compare problems across countries

## 📄 License

MIT License - Free for educational use

## 🤝 Contributing

Pull requests welcome! Add:
- New years/countries
- UI improvements
- Bug fixes

## 📞 Contact

For questions or suggestions, open an issue on GitHub.

---

**Made with 💙 for Math Olympiad enthusiasts worldwide**
