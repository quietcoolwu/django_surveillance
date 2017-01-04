$(function () {
  function a(a) {
    let t, e = a.getYear();
    e < 1900 && (e += 1900);
    let n = a.getMonth() + 1;
    n < 10 && (n = "0" + n);
    let i = a.getDate();
    return i < 10 && (i = "0" + i), t = e + "-" + n + "-" + i
  }

  function t(a, t) {
    $.getJSON(a, function (a) {
      let e = [], n = [], i = [];
      $.each(a, function (a, o) {
        a % t == 0 && (e.push(o.time), n.push(o.tmp), i.push(o.hmt))
      });
      let o = echarts.init(document.getElementById("env_data"));
      let option = {
        title: {text: "", subtext: ""},
        tooltip: {trigger: "axis"},
        legend: {data: ["温度(C)", "湿度(%)"]},
        toolbox: {
          show: !0,
          feature: {
            dataZoom: {yAxisIndex: "none"},
            dataView: {readOnly: !1},
            magicType: {type: ["line", "bar"]},
            restore: {},
            saveAsImage: {}
          }
        },
        xAxis: {type: "category", boundaryGap: !1, data: e},
        yAxis: {type: "value", axisLabel: {formatter: "{value} °C"}},
        series: [{
          name: "温度(C)",
          type: "line",
          data: n,
          markPoint: {data: [{type: "max", name: "最大值"}, {type: "min", name: "最小值"}]}
        }, {
          name: "湿度(%)",
          type: "line",
          data: i,
          markPoint: {data: [{type: "max", name: "最大值"}, {type: "min", name: "最小值"}]}
        }]
      };
      o.setOption(option)
    })
  }

  let e = new Date, n = "hour", i = "../static/data/" + n + "/" + a(e) + ".json";
  t(i, 1), $("#singleDateRange").DatePicker({startDate: moment()}), $("#submitit").click(function () {
    let a = $("#singleDateRange").val();
    n = "min";
    let e = "../static/data/" + n + "/" + a + ".json";
    t(e, 1)
  }), $("#changeit").click(function () {
    let a = $("#singleDateRange").val();
    n = "hour";
    let e = "../static/data/" + n + "/" + a + ".json";
    t(e, 1)
  })
});