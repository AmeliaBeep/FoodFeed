const copyLinkItems = document.querySelectorAll('.copy-link');

for (let item of copyLinkItems) {
    let link = item.getAttribute('href');
    item.addEventListener("click", (e) => {
        e.preventDefault();
        let textToCopy = window.location.href;
        textToCopy += link;
        navigator.clipboard.writeText(textToCopy)
        .then(() => {
        console.log('Link copied to clipboard!');
        })
  });
}