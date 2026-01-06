# 🌍 National Mathematical Olympiads - Problem Bank

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Live-brightgreen)](https://eisatopon.github.io/national-olympiads-bank/)

A comprehensive collection of mathematical olympiad problems from national competitions around the world, spanning from 1985 to 2025.

## 🎯 Features

- 🔍 **Advanced Search & Filtering**: Filter problems by year, country, competition type, and problem number
- 🌐 **Multiple Countries**: Problems from 11+ countries including China, Brazil, Iran, Philippines, Germany, Greece, India, Romania, Thailand, Turkey, and Vietnam
- 📝 **My Selection**: Save and organize your favorite problems
- 🖨️ **Print-Ready**: Export your problem sets for offline study
- 📱 **QR Code Sharing**: Generate shareable links for problem collections
- 📐 **LaTeX Support**: Full mathematical notation rendering with MathJax
- 🎨 **Beautiful UI**: Modern, responsive design with country flags

## 🌍 Included Countries

| Country | Flag | Coverage |
|---------|------|----------|
| 🇨🇳 China | ⭐ | 1985-2025 |
| 🇧🇷 Brazil | ⭐ | 1985-2025 |
| 🇮🇷 Iran | ⭐ | 1985-2025 |
| 🇵🇭 Philippines | ⭐ | 1985-2025 |
| 🇩🇪 Germany | ⭐ | 1985-2025 |
| 🇬🇷 Greece | ⭐ | 1985-2025 |
| 🇮🇳 India | ⭐ | 1985-2025 |
| 🇷🇴 Romania | ⭐ | 1985-2025 |
| 🇹🇭 Thailand | ⭐ | 1985-2025 |
| 🇹🇷 Turkey | ⭐ | 1985-2025 |
| 🇻🇳 Vietnam | ⭐ | 1985-2025 |

*More countries will be added continuously*

## 🏆 Competition Types

### National Olympiads
The primary national mathematics competition in each country, typically held annually to identify top mathematical talent.

### Selection Team Test
Advanced competitions used to select national teams for international competitions like IMO (International Mathematical Olympiad).

## 📊 Data Structure

Each year's problems are stored in JSON format:

```json
{
  "year": "2025",
  "problems": {
    "National Olympiads": {
      "China": [
        {
          "id": 1,
          "number": "1",
          "statement": "LaTeX formatted problem statement..."
        }
      ],
      "Brazil": [...]
    },
    "Selection Team Test": {
      "Iran": [...],
      "Philippines": [...]
    }
  }
}
```

## 🚀 Live Demo

Visit the live application: **[https://eisatopon.github.io/national-olympiads-bank/](https://eisatopon.github.io/national-olympiads-bank/)**

## 💻 Local Development

1. Clone the repository:
```bash
git clone https://github.com/Eisatopon/national-olympiads-bank.git
cd national-olympiads-bank
```

2. Open `index.html` in your browser:
```bash
# On macOS
open index.html

# On Linux
xdg-open index.html

# On Windows
start index.html
```

That's it! No build process required - pure HTML/CSS/JavaScript.

## 📁 Repository Structure

```
national-olympiads-bank/
├── index.html              # Main application
├── olympiads_2025.json     # Problems for 2025
├── olympiads_2024.json     # Problems for 2024
├── ...
├── olympiads_1985.json     # Problems for 1985
└── README.md               # This file
```

## 🔧 Configuration

To add your own JSON files, update the `DATA_URLS` object in `index.html`:

```javascript
const DATA_URLS = {
    "2025": "https://raw.githubusercontent.com/YOUR_USERNAME/national-olympiads-bank/main/olympiads_2025.json",
    "2024": "https://raw.githubusercontent.com/YOUR_USERNAME/national-olympiads-bank/main/olympiads_2024.json",
    // ... add more years
};
```

## 📚 Problem Coverage

| Year Range | Total Problems | Status |
|------------|----------------|--------|
| 2020-2025 | ~500 | ✅ Complete |
| 2010-2019 | ~800 | 🟡 In Progress |
| 2000-2009 | ~600 | 🟡 In Progress |
| 1990-1999 | ~500 | 🔴 Planned |
| 1985-1989 | ~300 | 🔴 Planned |

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Add Problems**: Submit problems from additional years or countries
2. **Fix Errors**: Report or fix typos, formatting issues, or incorrect solutions
3. **Translations**: Help translate problem statements
4. **New Features**: Suggest or implement new features

### How to Contribute

1. Fork the repository
2. Create a new branch (`git checkout -b feature/AmazingFeature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
5. Push to the branch (`git push origin feature/AmazingFeature`)
6. Open a Pull Request

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Mathematical problems are sourced from official national olympiad competitions
- Flag designs are simplified SVG representations
- Special thanks to all mathematics educators and olympiad organizers worldwide

## 📧 Contact

**Eisatopon** - GitHub: [@Eisatopon](https://github.com/Eisatopon)

Project Link: [https://github.com/Eisatopon/national-olympiads-bank](https://github.com/Eisatopon/national-olympiads-bank)

---

<div align="center">

### 🌟 If you find this project useful, please give it a star! 🌟

**Made with ❤️ for the mathematical community**

*Empowering students and educators worldwide through accessible olympiad resources*

</div>

## 🗺️ Roadmap

- [x] Basic problem bank interface
- [x] Search and filter functionality
- [x] LaTeX rendering support
- [x] QR code sharing
- [ ] Add more countries (USA, Russia, South Korea, etc.)
- [ ] Problem solutions and hints
- [ ] Difficulty ratings
- [ ] Topic tagging (Algebra, Geometry, Number Theory, Combinatorics)
- [ ] User accounts and progress tracking
- [ ] Mobile app version
- [ ] API for programmatic access

## 📈 Statistics

- **Total Problems**: 2,700+ (and growing)
- **Countries Covered**: 11
- **Years Covered**: 41 (1985-2025)
- **Competition Types**: 2
- **Languages**: English (more coming soon)

---

*Last Updated: January 2026*
