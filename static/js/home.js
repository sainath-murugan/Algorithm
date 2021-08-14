anime(
    {
        targets: '.hero .num ',
        innerHTML: [0, 100],
        easing: 'linear',
        round: 10,
        duration: 3000
    }
)


// bootstrap tool tip
var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
  return new bootstrap.Tooltip(tooltipTriggerEl)
})
