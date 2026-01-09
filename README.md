# Mathematical Olympiads Problem Bank 🌍

Μια ολοκληρωμένη τράπεζα θεμάτων από Εθνικές Μαθηματικές Ολυμπιάδες παγκοσμίως (1985-2025).

## ✨ Χαρακτηριστικά

### 🔍 Προηγμένη Αναζήτηση
- **Αναζήτηση με λέξεις-κλειδιά** στο περιεχόμενο των προβλημάτων
- Φίλτρα: Έτος, Χώρα, Τύπος Διαγωνισμού, Αριθμός Προβλήματος
- **Φίλτρο Δυσκολίας**: Easy, Medium, Hard
- **Κατηγορίες**: Algebra, Geometry, Combinatorics, Number Theory

### 💾 Αποθήκευση & Εξαγωγή
- **LocalStorage**: Αυτόματη αποθήκευση της επιλογής σου
- **PDF Export**: Εξαγωγή επιλεγμένων προβλημάτων σε PDF
- **Print**: Εκτύπωση με βελτιστοποιημένη μορφοποίηση
- **QR Code**: Δημιουργία QR για κοινοποίηση

### 📊 Στατιστικά
- Συνολικά προβλήματα
- Αριθμός χωρών
- Εύρος ετών
- Επιλεγμένα προβλήματα

### 🎨 Χαρακτηριστικά Interface
- Responsive design (mobile-friendly)
- MathJax για απόδοση μαθηματικών τύπων
- Σημαίες χωρών
- Dark mode ready (προαιρετικό)

## 🚀 Εγκατάσταση

### Βήμα 1: Δημιουργία GitHub Repository

1. Δημιούργησε νέο repository στο GitHub:
   - Όνομα: `olympiads-bank` (ή όποιο θέλεις)
   - Public repository
   - Πρόσθεσε README

### Βήμα 2: Προετοιμασία JSON Αρχείων

Κάθε έτος χρειάζεται ένα JSON αρχείο με τη δομή:

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

**Υποχρεωτικά πεδία:**
- `id`: Μοναδικός αριθμός (integer)
- `number`: Αριθμός προβλήματος (string)
- `statement`: Εκφώνηση προβλήματος (string με LaTeX)

**Προαιρετικά πεδία:**
- `category`: "Algebra" | "Geometry" | "Combinatorics" | "Number Theory"
- `difficulty`: "Easy" | "Medium" | "Hard"

### Βήμα 3: Upload στο GitHub

```bash
# Αρχεία που πρέπει να ανεβάσεις
olympiads_1985.json
olympiads_1986.json
...
olympiads_2025.json
```

### Βήμα 4: Ενημέρωση HTML

Στο αρχείο `olympiads_bank_enhanced.html`, άλλαξε το `YOUR_USERNAME`:

```javascript
const DATA_URLS = {
    "2025": "https://raw.githubusercontent.com/YOUR_USERNAME/olympiads-bank/main/olympiads_2025.json",
    "2024": "https://raw.githubusercontent.com/YOUR_USERNAME/olympiads-bank/main/olympiads_2024.json",
    // ...
}
```

### Βήμα 5: GitHub Pages (Προαιρετικό)

1. Settings → Pages
2. Source: Deploy from branch
3. Branch: main, folder: / (root)
4. Save

Το site θα είναι διαθέσιμο στο:
`https://YOUR_USERNAME.github.io/olympiads-bank/`

## 📝 Χρήση

### Αναζήτηση Προβλημάτων

1. **Επίλεξε έτος** (υποχρεωτικό)
2. Προαιρετικά φίλτρα:
   - Λέξη-κλειδί
   - Χώρα
   - Κατηγορία
   - Δυσκολία
   - Τύπος διαγωνισμού
   - Αριθμός προβλήματος
3. Πάτα "🔍 Search"

### Δημιουργία Επιλογής

1. Πάτα "✅ Add" σε κάθε πρόβλημα που θέλεις
2. Τα προβλήματα εμφανίζονται στο "📝 My Selection"
3. **Αυτόματη αποθήκευση** στο localStorage

### Εξαγωγή

- **📄 Export PDF**: Εξαγωγή σε PDF (χωρίς LaTeX rendering)
- **🖨️ Print**: Εκτύπωση (με LaTeX rendering)
- **📱 QR Code**: Δημιουργία QR για sharing
- **🗑️ Clear**: Καθαρισμός επιλογής

## 🎯 Tips για JSON Creation

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

- **Easy**: Προβλήματα για αρχάριους (P1-P2 συνήθως)
- **Medium**: Μέτρια δυσκολία (P3-P4)
- **Hard**: Δύσκολα προβλήματα (P5-P6, Selection Tests)

### Category Assignment

- **Algebra**: Ανισότητες, εξισώσεις, πολυώνυμα
- **Geometry**: Τρίγωνα, κύκλοι, γεωμετρικές ιδιότητες
- **Combinatorics**: Μέτρηση, γραφήματα, αρχές
- **Number Theory**: Πρώτοι, διαιρετότητα, modular arithmetic

## 🛠️ Προσαρμογές

### Προσθήκη Χωρών

1. Πρόσθεσε στο `<select id="country">`:
```html
<option value="USA">USA</option>
```

2. Προαιρετικά: Πρόσθεσε σημαία στο `.flags-banner`

### Προσθήκη Κατηγοριών

```html
<select id="category">
    <option value="Functional Equations">Functional Equations</option>
</select>
```

### Custom Styling

Άλλαξε τα χρώματα στο CSS:

```css
.header {
    background: linear-gradient(135deg, #your-color-1, #your-color-2);
}
```

## 📱 Responsive Design

- Desktop: Full grid layout
- Tablet: 2-column layout
- Mobile: Single column, optimized buttons

## 🔧 Τεχνικές Λεπτομέρειες

### Libraries Used

- **MathJax 3**: Για rendering LaTeX
- **jsPDF**: Για PDF generation
- **QRCode.js**: Για QR code generation

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

Δες το `olympiads_2024_example.json` για πλήρες παράδειγμα.

## 🐛 Troubleshooting

### Προβλήματα Loading

1. **404 Error**: Έλεγξε ότι το URL είναι σωστό
2. **CORS Error**: Χρησιμοποίησε GitHub Pages ή local server
3. **Math not rendering**: Περίμενε λίγο, το MathJax φορτώνει

### LocalStorage Issues

```javascript
// Clear cache
localStorage.clear();
location.reload();
```

## 🎓 Use Cases

- Προετοιμασία για διαγωνισμούς
- Δημιουργία εξετάσεων
- Μελέτη ανά κατηγορία/δυσκολία
- Σύγκριση προβλημάτων χωρών

## 📄 License

MIT License - Ελεύθερο για εκπαιδευτική χρήση

## 🤝 Contributing

Pull requests welcome! Προσθέστε:
- Νέα έτη/χώρες
- Βελτιώσεις UI
- Bug fixes

## 📞 Contact

Για ερωτήσεις ή προτάσεις, άνοιξε issue στο GitHub.

---

**Made with 💙 for Math Olympiad enthusiasts worldwide**
