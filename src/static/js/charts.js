const colores = ['#4caf50', '#f44336', '#2196f3', '#ff9800', '#9c27b0', '#00bcd4', '#e91e63'];

const getOptionChart1 = () => {
    const categorias = categoriaData.map(item => item[0]);
    const valores = categoriaData.map(item => item[1]);

    return {
        color: colores,
        tooltip: { trigger: 'axis' },
        xAxis: {
            type: 'category',
            data: categorias,
            axisLabel: { interval: 0, rotate: 30 }
        },
        yAxis: { type: 'value' },
        series: [{
            name: 'Profesores',
            type: 'bar',
            barWidth: '60%',
            data: valores
        }]
    };
};


const getOptionChart2 = () => {
    const datos = generoData.map(item => ({ value: item[1], name: item[0] }));

    return {
        color: colores,
        tooltip: { trigger: 'item' },
        legend: {
            top: '5%',
            left: 'center',
            textStyle: {
                fontSize: 14
            }
        },
        series: [{
            name: 'Género',
            type: 'pie',
            radius: ['40%', '70%'],
            avoidLabelOverlap: false,
            itemStyle: {
                borderRadius: 10,
                borderColor: '#fff',
                borderWidth: 2
            },
            label: { show: false },
            emphasis: {
                label: {
                    show: true,
                    fontSize: 20,
                    fontWeight: 'bold'
                }
            },
            labelLine: { show: false },
            data: datos
        }]
    };
};

const getOptionChart3 = () => {
    const grados = gradoData.map(item => item[0]);
    const valores = gradoData.map(item => item[1]);

    return {
        color: colores,
        tooltip: {
            trigger: 'axis',
            axisPointer: { type: 'shadow' }
        },
        grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
        },
        xAxis: { type: 'value' },
        yAxis: {
            type: 'category',
            data: grados,
            axisLabel: { fontSize: 12 }
        },
        series: [{
            name: 'Profesores',
            type: 'bar',
            barWidth: '50%',
            data: valores
        }]
    };
};


const initCharts = () => {
    const chart1 = echarts.init(document.getElementById('chart1'));
    const chart2 = echarts.init(document.getElementById('chart2'));
    const chart3 = echarts.init(document.getElementById('chart3'));

    chart1.setOption(getOptionChart1());
    chart2.setOption(getOptionChart2());
    chart3.setOption(getOptionChart3());
}

window.addEventListener('load', () => {
    initCharts();
});