
# 📘 React Notes

## ✅ What is React?

- A **JavaScript library** for building **user interfaces**
- Maintained by **Meta (Facebook)**
- Uses a **component-based** architecture
- **Declarative** UI: You describe *what* to render, not *how*

---

## ⚙️ Core Concepts

### 1. Components

- **Functional Components** (modern)
- **Class Components** (legacy)

```js
function Welcome(props) {
  return <h1>Hello, {props.name}</h1>;
}
class Welcome extends React.Component {
  render() {
    return <h1>Hello, {this.props.name}</h1>;
  }
}
```

---

## 1️⃣ JSX Compilation and Execution Flow

### 🧩 Example Code
```jsx
function App() {
  return <h1>Hello, React!</h1>;
}

ReactDOM.render(<App />, document.getElementById('root'));
```

---

### 🔄 Compilation Step-by-Step

#### ➤ Step 1: JSX to JavaScript (via Babel)
JSX is not valid JavaScript. Tools like Babel convert it into `React.createElement` calls:

```js
const App = () => {
  return React.createElement('h1', null, 'Hello, React!');
};
```

#### ➤ Step 2: ReactDOM.render
This tells React to:
- Create a **Virtual DOM** representation of the component
- Mount it to the real DOM element with `id="root"`

---

## 2️⃣ What is the Virtual DOM?

### 💡 Concept
- A **lightweight copy** of the actual DOM
- Kept in memory by React
- Allows fast comparisons between UI states

### 🔍 How It Works:
1. React builds a **Virtual DOM Tree** using `React.createElement()`
2. When state/props change, React:
   - Creates a **new Virtual DOM**
   - **Diffs** the new tree with the previous one (Diffing Algorithm)
   - **Batches & updates** only the changed parts in the **Real DOM** (Reconciliation)

---

### 🔄 Example Flow

#### Initial Render:
```jsx
<div>Hello</div>
```
Virtual DOM:
```js
{ type: 'div', props: { children: 'Hello' } }
```

#### After State Update:
```jsx
<div>Hello World</div>
```

React:
- Creates new Virtual DOM: `{ type: 'div', props: { children: 'Hello World' } }`
- Diffs with old
- Finds change in text node
- Updates **only that node** in the Real DOM ✅

---

## 3️⃣ How React is Different from Other JS Libraries

| Feature                | React                         | Traditional JS (e.g., jQuery)      | Angular/Vue               |
|------------------------|-------------------------------|------------------------------------|----------------------------|
| **Approach**           | Declarative                   | Imperative                         | Declarative                |
| **Rendering**          | Virtual DOM                   | Direct DOM Manipulation            | Virtual DOM (Vue), real DOM (Angular) |
| **Component Model**    | Function/Class Components     | None (custom logic)                | Templates + Components     |
| **Data Binding**       | One-way (unidirectional)      | Manual or bidirectional (jQuery)   | Two-way (Angular), One-way (Vue default) |
| **Performance**        | Efficient (diffing + batching)| Less efficient                     | Depends on usage           |
| **Learning Curve**     | Moderate                      | Easy                               | Angular = steep, Vue = easy |
| **Tooling**            | Modern Ecosystem (CRA, Vite)  | Minimal                            | CLI tools provided         |

---

## 📦 Summary

- React uses **JSX**, compiled to JavaScript via **Babel**
- React builds a **Virtual DOM** to optimize UI updates
- Only changed parts of the UI are updated in the real DOM
- React is **declarative, component-based**, and promotes **clean architecture**
- Compared to jQuery or Angular, React offers:
  - Better performance
  - Easier maintenance
  - Better testability and reuse

---

## 🔗 Bonus: Tools Behind the Scenes

| Tool         | Purpose                         |
|--------------|----------------------------------|
| Babel        | Transpiles JSX to JS            |
| Webpack/Vite | Bundles JS/CSS into browser-ready files |
| React DevTools | Debug React components         |
| ESLint       | Static code checking             |
| Prettier     | Code formatting                  |

---
