---
name: frontend-design
description: ULTRA-CONSOLIDATED frontend, creative, and visual design -- UI design, web components, pages, dashboards, React components, HTML/CSS/Tailwind layouts, algorithmic art (p5.js with seeded randomness, flow fields, particles, generative patterns), data visualization (Tufte principles for data-ink ratio and chartjunk elimination, AntV infographic syntax), and BLING usability audits. Use for ANY visual, creative, or design output.
version: "2.0"
triggers: ["UI", "design", "frontend", "page", "styling", "visual", "BLING", "web component", "dashboard", "React", "Tailwind", "shadcn", "HTML", "CSS", "landing page", "web app", "beautify", "poster", "art", "generative art", "algorithmic art", "creative coding", "p5.js", "flow field", "particle system", "seeded randomness", "visualization", "chart", "graph", "Tufte", "infographic", "data-ink", "chartjunk", "AntV", "D3", "SVG", "canvas", "WebGL", "data viz", "graphical integrity", "usability audit", "color", "typography", "spacing", "animation", "brand", "layout", "responsive", "accessibility"]
related: ["cloudflare"]
priority: 2
platform: all
autonomous: false
self_sufficient: true
---

# FRONTEND -- v2.0 (Ultra-Consolidated Creative + Visual)

> **Merges 3:** frontend-design + algorithmic-art + data-visualization
> **Related:** Load `cloudflare` for deploying frontend assets to Cloudflare Pages/R2/Workers.
> **Cloudflare Full-Stack:** All web UI deployed to Cloudflare Pages. Static assets on R2. Dynamic rendering via Workers.

## execute_plan

update_plan([
  {"step": "Identify output type: web UI, algorithmic art, or data visualization", "status": "pending"},
  {"step": "Design and build with appropriate framework (React, p5.js, D3, AntV)", "status": "pending"},
  {"step": "Apply Tufte principles if data; verify originality if art; audit if UI", "status": "pending"},
  {"step": "Verify: design quality, responsiveness, accessibility baseline, deployment", "status": "pending"},
])

---

## Web UI Design

### Design System (LOCKED v3.0)
```css
:root {
  --blue: #1a56db;
  --blue-dark: #1040a8;
  --blue-light: #dbeafe;
  --blue-subtle: #eff6ff;
  --blue-mid: #6094e8;
  --text: #1a1a2e;
  --text-muted: #6b7280;
  --bg: #ffffff;
  --border: #e5e7eb;
  --card-bg: #f9fafb;
  --max-w: 960px;
  --radius: 8px;
}
```

### Fonts
- **Headings/Nav/Meta:** Inter (sans-serif)
- **Body:** Source Serif 4 (serif)
- **Code:** JetBrains Mono (monospace)
- **Dark themes FORBIDDEN.** Light theme only.

### Mandatory Components
- **Sticky Top Nav:** `backdrop-blur` effect, fixed position
- **AI Query Box:** Distinct styled input for AI-powered search
- **Related Papers Section:** Grid of paper cards with hover shadow
- **Paper Cards:** Title, author, abstract snippet, DOI link
- **Badges:** DOI (blue), Type (purple), Category (green), Tag (gray), License (orange)

### Framework Stack
- **React** + TypeScript for component architecture
- **Tailwind CSS** for utility-first styling
- **shadcn/ui** for accessible component primitives
- **No generic AI aesthetics.** Creative, polished, original designs only.

### BLING Usability Audit
After every UI change, answer these 4 questions for EVERY element:
1. **WHAT'S WORKING?** -- What meets the design spec?
2. **WHAT'S NOT?** -- What fails the spec or is broken?
3. **WHAT NEEDS TO BE FIXED?** -- Blocking issues requiring immediate fix
4. **WHAT CAN BE IMPROVED/ENHANCED?** -- Non-blocking polish items

Audit dimensions: typography, color, spacing, animation, brand distinctiveness, responsive behavior, accessibility baseline (WCAG 2.1 AA contrast minimums).

### Responsive Breakpoints
```css
/* Mobile first */
/* sm: 640px, md: 768px, lg: 1024px, xl: 1280px */
```

---

## Algorithmic Art

### Core Principles
- **Originality:** NEVER copy existing artists' work. Create original generative compositions.
- **Reproducibility:** All art must use `randomSeed()` with a documented seed value.
- **Interactivity:** Expose parameters via sliders or query params for exploration.

### p5.js Template
```javascript
let seed = 42;
let particles = [];
let flowField;

function setup() {
  createCanvas(800, 800);
  randomSeed(seed);
  noiseSeed(seed);
  
  // Flow field -- Perlin noise vectors
  flowField = new Array(floor(width / 10) * floor(height / 10));
  
  // Particle system
  for (let i = 0; i < 200; i++) {
    particles.push(new Particle(random(width), random(height)));
  }
  
  // Parameter controls
  createP('Seed').position(10, height + 10);
  let seedSlider = createSlider(0, 1000, seed);
  seedSlider.position(60, height + 10);
  seedSlider.input(() => { seed = seedSlider.value(); reset(); });
}

function draw() {
  background(255, 10); // Fade trail
  for (let p of particles) {
    p.follow(flowField);
    p.update();
    p.show();
    p.edges();
  }
}
```

### Generative Techniques
| Technique | p5.js Implementation | Parameters |
|:----------|:---------------------|:-----------|
| **Flow Field** | Perlin noise vectors, particle advection | noiseScale, particleCount, trailOpacity |
| **Particle System** | Array of Particle objects with velocity/acceleration | count, speed, lifespan, color palette |
| **Voronoi Tessellation** | Random seed points, Fortune's algorithm | siteCount, metric (Euclidean/Manhattan) |
| **L-System** | Recursive string rewriting | axiom, rules, iterations, angle |
| **Reaction-Diffusion** | Gray-Scott model on 2D grid | feedRate, killRate, diffusionA, diffusionB |
| **Wave Function Collapse** | Tile adjacency constraints | tileSet, outputSize, periodic boundary |

### Color Palettes
Export a `colors` array that the art references. Use `lerpColor()` for smooth transitions. Pre-define palettes; never generate fully random colors.

---

## Data Visualization

### Tufte's Five Principles
1. **Data-Ink Ratio:** Maximize ink devoted to data. Erase non-data ink. Erase redundant data-ink.
2. **Chartjunk Elimination:** Remove decoration, moire vibration, grids, ornamental borders. Every mark must carry information.
3. **Graphical Integrity:** Lie Factor = (size of effect in graphic) / (size of effect in data). Must equal 1.0 ± 0.05.
4. **Small Multiples:** Use repeated small charts for comparison across categories. Same axes, different data.
5. **Data Density:** Maximize data points per unit area. Graphics should be data-rich.

### Chart Selection Matrix
| Data Type | Best Chart | Why | Avoid |
|:----------|:-----------|:----|:------|
| **Time series** | Line chart | Shows trend direction + rate | Area chart (hides baseline) |
| **Categories** | Horizontal bar chart | Labels readable, length comparison easy | Vertical bar (cramped labels) |
| **Parts of whole** | Bar chart | Accurate area comparison | Pie chart (angle comparison is poor) |
| **Distribution** | Histogram | Shows shape of data | Box plot (hides multimodal) |
| **Correlation** | Scatter plot | Shows relationship patterns | Bubble chart (area distortion) |
| **Ranking** | Sorted bar chart | Immediate rank visibility | Dot plot (harder to compare) |
| **Flow/process** | Sankey diagram | Shows magnitude + direction | Funnel (ordered only) |

### Infographic Syntax (AntV)
```yaml
infographic column-chart:
  title: "Paper Publications by Year"
  data:
    - year: 2024, count: 12
    - year: 2025, count: 47
    - year: 2026, count: 89
  theme: light
  settings:
    xAxis: year
    yAxis: count
    color: "#1a56db"
    showValues: true
```

### Graphical Integrity Checklist
- [ ] Y-axis starts at zero (or truncation is clearly marked)
- [ ] All axes labeled with units
- [ ] No 3D effects on 2D data (volume distorts perception)
- [ ] Gridlines at 10% opacity or removed
- [ ] Legend present and readable
- [ ] Data source cited below chart

## Anti-Patterns
| Anti-Pattern | Fix |
|:-------------|:----|
| Generic AI aesthetics | Custom design system (LOCKED v3.0 tokens) |
| 3D charts for 2D data | 3D distorts perception -- use 2D always |
| Pie charts with >5 slices | Sorted bar chart |
| No axis labels | Always label both axes with units |
| Truncated y-axis without marking | Start at zero OR add break marker |
| Copying existing artists' work | Original compositions with seeded randomness |
| Generative art without seed | Always document seed for reproducibility |
