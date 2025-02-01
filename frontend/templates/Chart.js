<button id="downloadBtn{{ loop.index }}">ダウンロード</button>
<script>
    document.getElementById('downloadBtn{{ loop.index }}').addEventListener('click', function() {
        var canvas = document.getElementById('cpuChart{{ loop.index }}');
        var image = canvas.toDataURL('image/png');
        
        var link = document.createElement('a');
        link.href = image;
        link.download = 'cpu_usage_chart.png';
        link.click();
    });
</script>
