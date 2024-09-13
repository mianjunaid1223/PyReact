function copyCode(button) {{
    const pre = button.parentElement.querySelector('pre');
    const code = pre.textContent;
    navigator.clipboard.writeText(code).then(() => {{
        button.textContent = 'Copied!';
        setTimeout(() => {{
            button.textContent = 'Copy';
        }}, 2000);
    }});
}}

document.body.onchange(() => {{
    document.querySelectorAll('.mockup-code')?.forEach(child => {
        child.parentElement.classList.add('.parent');
      });
      
    }})
document.body.onload(() => {{
    document.querySelectorAll('.mockup-code')?.forEach(child => {
        child.parentElement.classList.add('.parent');
      });
      
}})