/** @type {import('tailwindcss').Config} */
module.exports = {
content: [
"./templates/**/*.html", // Templates at the project level
"./**/templates/**/*.html",
'./static/js/**/*.js', // JavaScript files
],
theme: {
extend: {},
},
plugins: [],
};