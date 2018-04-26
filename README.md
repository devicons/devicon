# Devicon v2

[http://konpa.github.io/devicon/](http://konpa.github.io/devicon/)

Devicon consiste en reunir iconos, logos o marcas de todas las herramientes de desarrollo posibles.
Cada icono viene en diferentes versiones: font/svg, original/plain/line, colored/not colored, wordmark/no wordmark.

Devicon tiene 78 iconos y mas de 200 versiones, y aun sige creciendo.

[Ver todos los iconos disponibles.](http://konpa.github.io/devicon/)

## Icon requests

**Si quieren algun icono en particular, dejar comentarios [aqui](https://github.com/konpa/devicon/issues/11).**

## Como usar

Para una rapida instalacion visita [devicon.fr](http://konpa.github.io/devicon/)

_2 maneras de usar devicon:_

#### Iconos SVG

- Copia y pega el codigo del SVG (desde su respectiva [carpeta](https://github.com/konpa/devicon/tree/master/icons) o de la [pagina del proyecto](http://konpa.github.io/devicon/))

```html
<!-- para una version plana -->
<svg class="devicon-git-plain" viewBox="0 0 128 128">
  <path fill="#F34F29" d="M124.742,58.378L69.625,3.264c-3.172-3.174-8.32-3.174-11.497,0L46.685,14.71l14.518,14.518c3.375-1.139,7.243-0.375,9.932,2.314c2.703,2.706,3.462,6.607,2.293,9.993L87.42,55.529c3.385-1.167,7.292-0.413,9.994,2.295c3.78,3.777,3.78,9.9,0,13.679c-3.78,3.78-9.901,3.78-13.683,0c-2.842-2.844-3.545-7.019-2.105-10.521L68.578,47.933l-0.002,34.341c0.922,0.455,1.791,1.063,2.559,1.828c3.779,3.777,3.779,9.898,0,13.683c-3.779,3.777-9.904,3.777-13.679,0c-3.778-3.784-4.088-9.905-0.311-13.683C58.079,83.169,59,82.464,60,81.992V47.333c-1-0.472-1.92-1.172-2.856-2.111c-2.861-2.86-3.396-7.06-1.928-10.576L40.983,20.333L3.229,58.123c-3.175,3.177-3.155,8.325,0.02,11.5l55.126,55.114c3.173,3.174,8.325,3.174,11.503,0l54.86-54.858C127.913,66.703,127.916,61.552,124.742,58.378z"/>
</svg>
```

- Agrega reglas css a tu hoja de estilos
```css
.devicon-git-plain {
  max-width: 2em;
}

/* Si quieres cambiar el color original */
.devicon-git-plain path {
  fill: #4691f6;
}
```

#### Iconos como fuente

- Agrega el archivo devicon.css y los archivos de las fuentes a tu proyecto

```html
  <link rel="stylesheet" href="devicon.css">

  <!-- if you want colored versions -->
  <link rel="stylesheet" href="devicon-colors.css">
```

- Agrega el icono usando la etiqueta <i>

```html
  <!-- para la version plain -->
  <i class="devicon-git-plain"></i>

  <!-- para la version plain con wordmark -->
  <i class="devicon-git-plain-wordmark"></i>

  <!-- para la version plain con color principal (devicon-color.css o devicon.min.css requeridos) -->
  <i class="devicon-git-plain colored"></i>

  <!-- para la version plana con wordmark y con el color principal (devicon-color.css o devicon.min.css requeridos) -->
  <i class="devicon-git-plain-wordmark colored"></i>
```

##### NPM and Bower packages

Puedes instalar devicon como dependencia a tus proyectos usando NPM o Bower

```
  // NPM
  npm install --save devicon
  
  // Bower
  bower install --save devicon
```

<sub>La fuente final esta hecha con [Icomoon app](https://icomoon.io/)</sub>

##### Ver el [archivo devicon.json](https://github.com/konpa/devicon/blob/master/devicon.json) o la [pagina de devicon](http://konpa.github.io/devicon/) para ver la lista completa de iconos en todas sus versiones disponibles.

## Contribuir

Heche un vistazo al archivo CONTRIBUTING.md

Bajo [Licencia MIT](https://github.com/konpa/devicon/blob/master/LICENSE)

<sub>All product names, logos, and brandsare property of their respective owners. All company, product and service names used in this website are for identification purposes only. Use of these names, logos, and brands does not imply endorsement.</sub>
