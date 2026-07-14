<div align="center">

# 🐉 DragonStats

### Build Your Own Dynamic GitHub SVG Cards with Java & Spring Boot

Create beautiful, customizable GitHub profile cards, language cards, badges and developer analytics that can be embedded anywhere.

Designed to be self-hostable, extensible and open source.

<p>

<img src="https://img.shields.io/github/stars/DragonB0i/DragonStats?style=for-the-badge"/>
<img src="https://img.shields.io/github/forks/DragonB0i/DragonStats?style=for-the-badge"/>
<img src="https://img.shields.io/github/license/DragonB0i/DragonStats?style=for-the-badge"/>
<img src="https://img.shields.io/badge/Java-21-orange?style=for-the-badge&logo=openjdk"/>
<img src="https://img.shields.io/badge/Spring_Boot-3-success?style=for-the-badge&logo=springboot"/>

</p>

</div>

---

# ✨ What is DragonStats?

DragonStats is an open-source REST API that generates beautiful **dynamic SVG cards** using live GitHub data.

Unlike static badges, DragonStats fetches your GitHub profile in real time and renders modern SVG cards that can be embedded directly into your README.

Perfect for:

- GitHub Profiles
- Portfolio Websites
- Personal Dashboards
- Documentation
- Developer Portfolios

---

# 🚀 Features

- 🎨 Modern SVG Cards
- 👤 Profile Card
- 💻 Language Card
- 📊 Dynamic GitHub Statistics
- 🌙 Multiple Themes
- ⚡ Fast REST API
- 🔄 Automatic Live Updates
- ☁️ Self Host Friendly
- ❤️ Open Source

---

# 🌐 Demo

```text
https://your-domain.com/api?username=DragonB0i
```

---

# 📦 Available Endpoints

| Endpoint | Description |
|-----------|-------------|
| `/api` | Profile Statistics Card |
| `/languages` | Languages Card |
| `/badge/profile` | Compact Profile Badge |
| `/badge/activity` | Activity Badge |
| `/repositories` | Repository Card *(WIP)* |
| `/streak` | Streak Card *(Planned)* |
| `/overview` | Dashboard *(Planned)* |
| `/rank` | Rank Card *(Planned)* |
| `/trophy` | Trophy Card *(Planned)* |

---

# 📸 Example

```md
![Stats](https://your-domain.com/api?username=YOUR_USERNAME)

![Languages](https://your-domain.com/languages?username=YOUR_USERNAME)
```

---

# 🛠️ Running Locally

Clone the repository

```bash
git clone https://github.com/DragonB0i/DragonStats.git
```

Move into the project

```bash
cd DragonStats
```

Run Spring Boot

```bash
./mvnw spring-boot:run
```

or

```bash
mvn spring-boot:run
```

The server will start on

```
http://localhost:8080
```

---

# ☁️ Deploy Your Own

You can deploy DragonStats in minutes using:

- Render
- Railway
- Fly.io
- Docker
- VPS
- Azure
- AWS
- Google Cloud

Simply fork the repository, deploy it, and replace the API URL with your own deployment.

Example:

```text
https://your-domain.com/api?username=YOUR_USERNAME
```

---

# 🔧 Configuration

DragonStats uses the GitHub REST API.

No database is required.

Simply deploy and start using it.

---

# 🤝 Contributing

Contributions are welcome!

Ideas include:

- New card designs
- More themes
- Better animations
- GraphQL integration
- Performance improvements
- Additional GitHub analytics
- Bug fixes

Feel free to:

⭐ Star the project

🍴 Fork it

🐛 Open Issues

🚀 Submit Pull Requests

---

# 🗺️ Roadmap

- ✅ Profile Card
- ✅ Language Card
- ✅ Themes
- ✅ Caching
- 🔄 Repository Card
- 🔄 Rank Card
- 🔄 Trophy Card
- 🔄 Streak Card
- 🔄 Dashboard
- 🔄 Activity Graph
- 🔄 Heatmap
- 🔄 GraphQL Support
- 🔄 PNG Export
- 🔄 API Documentation

---

# 📄 License

This project is licensed under the MIT License.

---

<div align="center">

### ⭐ If you find DragonStats useful, consider starring the repository!

Help us make beautiful GitHub profiles accessible to everyone.

Made with ❤️ using Java & Spring Boot

</div>
