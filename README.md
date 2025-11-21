<p align="center">
  <img src="https://raw.githubusercontent.com/MipaSenpai/Polygons/main/.github/images/icon.svg" width="120" alt="Polygons Logo">
</p>

<h1 align="center">🛡️ Polygons</h1>
<p align="center">
  <strong>Territory protection system for Endstone & LeviLamina servers</strong>
</p>

<p align="center">
  <a href="https://github.com/MipaSenpai/Polygons/stargazers">
    <img src="https://img.shields.io/github/stars/MipaSenpai/Polygons?style=for-the-badge&logo=github&color=8A2BE2&logoColor=white" />
  </a>
  <a href="https://github.com/MipaSenpai/Polygons/issues">
    <img src="https://img.shields.io/github/issues/MipaSenpai/Polygons?style=for-the-badge&logo=github&color=4B0082&logoColor=white" />
  </a>
  <a href="https://github.com/MipaSenpai/Polygons/blob/main/LICENSE">
    <img src="https://img.shields.io/badge/license-MIT-9400D3?style=for-the-badge&logoColor=white" />
  </a>
  <img src="https://img.shields.io/badge/python-3.9+-7C83FD?style=for-the-badge&logo=python&logoColor=white" />
</p>

<p align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=18&pause=1000&color=8A2BE2&center=true&vCenter=true&width=600&lines=Protect+your+territory+with+one+command;Lightning-fast+spatial+queries;SQLite+%7C+MySQL+%7C+PostgreSQL;Built+for+performance+and+simplicity" alt="Typing SVG" />
</p>

---

## ✨ What is Polygons?

Polygons is a **lightweight, high-performance territory protection plugin** for Minecraft Bedrock servers running on Endstone & LeviLamina. Create protected zones with a single block placement, manage permissions through intuitive forms, and enjoy blazing-fast spatial queries powered by R-tree indexing.

> 💜 **One command. Multiple databases. Zero lag.**  
> No complex setup. No performance overhead. Just protection.

---

## 🚀 Key Features

<table>
<tr>
<td width="50%">

### ⚡ Lightning Fast
**R-tree spatial indexing** ensures instant polygon lookups even with thousands of protected areas. No lag, no delays.

### 🗄️ Database Flexibility
Choose your storage: **SQLite**, **MySQL**, or **PostgreSQL**. Switch between them with a single config change.

### 💾 Smart Caching
In-memory cache with automatic synchronization keeps queries fast and data consistent across restarts.

</td>
<td width="50%">

### 🎮 One-Command Management
**`/polygon`** — that's it. Create, configure, and manage all your territories through one intuitive command with form-based UI.

### 👥 Member Management
Add friends to your polygon, configure granular permissions, and control who can build, break, or access chests.

### 🎨 Customizable Sizes
Define polygon sizes per block type.

</td>
</tr>
</table>

---

## 📦 Installation

Download the latest plugin file from [Releases](https://github.com/MipaSenpai/Polygons/releases) and place it in your server's `plugins` folder. Restart the server.

**For LeviLamina**: You need to have [LeviStone](https://github.com/LiteLDev/LeviStone) installed.

Restart your server. Done!

---

## 🎮 Usage

### Visual Borders

To visualize polygon boundaries in-game, install the resource pack:  
[LiteLoaderBDS-CUI v1.1](https://github.com/OEOTYAN/LiteLoaderBDS-CUI/releases/tag/v1.1)

### Creating a Polygon

1. Place a **diamond block** or **stone** (configurable) in the world
2. Enter a unique name for your polygon
3. Your territory is now protected!

### Managing Polygons

Use the `/polygon` (or `/pg`) command to open the management menu:

| Action | Description |
|--------|-------------|
| **View Polygons** | List all your protected territories |
| **Manage Flags** | Configure break/place/chest permissions |
| **Add Member** | Invite players to your polygon |
| **Remove Member** | Revoke access from players |
| **Delete Polygon** | Remove protection (owner only) |

---

## ⚙️ Configuration

Edit `plugins/polygons/config.toml`:

### Database Settings

```toml
[database]
type = "sqlite"  # Options: "sqlite", "mysql", "postgresql"

[database.sqlite]
filename = "polygons.db"

[database.mysql]
host = "localhost"
port = 3306
username = "root"
password = "password"
database = "polygons"

[database.postgresql]
host = "localhost"
port = 5432
username = "postgres"
password = "password"
database = "polygons"
```

**Switch databases anytime** — just change the `type` field and restart!

---

### Polygon Types

Define which blocks create polygons and their sizes:

```toml
[polygonTypes]
"minecraft:diamond_block" = 7   # 7x7x7 area
"minecraft:stone" = 9           # 9x9x9 area
"minecraft:gold_block" = 15     # 15x15x15 area
```

---

### Permission Flags

Each polygon has three configurable flags:

| Flag | Description | Default |
|------|-------------|---------|
| `canBreak` | Allow non-members to break blocks | `false` |
| `canPlace` | Allow non-members to place blocks | `false` |
| `canOpenChests` | Allow non-members to open containers | `false` |

Owners and members always have full access.

---

## 🎯 Performance Benchmarks

### Cache Loading & Memory

| Polygons | Load Time | Memory Usage | Lookup Speed |
|----------|-----------|--------------|--------------|
| 100      | 0.003s    | 2.1 MB       | 0.020 ms     |
| 1,000    | 0.029s    | 9.3 MB       | 0.020 ms     |
| 10,000   | 0.718s    | 109.8 MB     | 0.025 ms     |
| 50,000   | 3.908s    | 499.7 MB     | 0.032 ms     |

### Game Actions (average response time)

| Polygons | Block Break | Block Place | Chest Access |
|----------|-------------|-------------|--------------|
| 100      | 0.021 ms    | 0.021 ms    | 0.021 ms     |
| 1,000    | 0.022 ms    | 0.024 ms    | 0.021 ms     |
| 10,000   | 0.030 ms    | 0.028 ms    | 0.027 ms     |
| 50,000   | 0.034 ms    | 0.028 ms    | 0.042 ms     |

**Maximum throughput:** 28,839 actions/second

Even with 50,000 polygons, all actions complete in under 0.05ms. Zero lag guaranteed.

---

## 🛡️ Protection Features

- Prevents unauthorized block placement
- Prevents unauthorized block breaking
- Checks polygon boundaries in 3D space
- Protects chests, barrels, shulker boxes, ender chests
  
---

## 🤝 Contributing

Contributions are welcome! Fork the repo, make your changes, and open a Pull Request.

---

## 📜 License

This project is licensed under the **MIT License**. See [LICENSE](LICENSE) for details.

---

## 🛠️ Tech Stack

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white" />
  <img src="https://img.shields.io/badge/R--tree-8A2BE2?style=for-the-badge&logoColor=white" />
  <img src="https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white" />
  <img src="https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white" />
  <img src="https://img.shields.io/badge/PostgreSQL-336791?style=for-the-badge&logo=postgresql&logoColor=white" />
</p>

---

<p align="center">
  <sub>✨ Polygons - where performance meets simplicity. ✨</sub>
</p>
