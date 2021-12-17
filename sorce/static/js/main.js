window.onload = function(){
    const ctx = document.getElementById('myChart');
    var posiRatioStr = document.getElementById('posiRatio').value;
    var negaRatioStr = document.getElementById('negaRatio').value;
    var posiRatio = parseFloat(posiRatioStr);
    var negaRatio = parseFloat(negaRatioStr);

    var myChart = new Chart(ctx, {
      type: 'pie',
      data: {
        labels: ['ポジティブ', 'ネガティブ'],
        datasets: [{
          data: [posiRatio, negaRatio],
          backgroundColor: ['#66FF66', '#FF6666'],
          weight: 10,
        }],
      },
    });
}

function sample(){
    var subject = document.getElementById('review1');
    if(subject.classList.contains('close')){
        subject.classList.remove('close');
    } else {
        subject.classList.add('close');
    }
}



function closeWindow(names){
    var subject = document.getElementById(names);
    if(subject.classList.contains('close')){
        subject.classList.remove('close');
    } else {
        subject.classList.add('close');
    }
}