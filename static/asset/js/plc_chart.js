/**
 * Created by wukai on 2016/12/26.
 */

$(function () {
  function get_time(target) {
    var t, e = target.getYear();
    e < 1900 && (e += 1900);
    var n = target.getMonth() + 1;
    n < 10 && (n = "0" + n);
    var i = target.getDate();
    return i < 10 && (i = "0" + i), t = e + "-" + n + "-" + i
  }

  function get_data(source, target) {
    $.getJSON(source, function (a) {
      var e = [], n = [], i = [], h = [];
      $.each(a, function (a, item) {
        a % target == 0 && (e.push(item.time), n.push(item.gun_location), i.push(item.gun_speed), h.push(item.input_material_speed))
      });
      var chart = echarts.init(document.getElementById("plc_data"));
      var option = {
        title: {text: "", subtext: ""},
        tooltip: {trigger: "axis"},
        legend: {data: ["枪架位置(mm)", "枪架速度(mm/s)", "送料速度(m/min)"]},
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
        yAxis: {type: "value", axisLabel: {formatter: "{value}"}},
        series: [{
          name: "枪架位置(mm)",
          type: "line",
          data: n,
          markPoint: {data: [{type: "max", name: "最大值"}, {type: "min", name: "最小值"}]}
        }, {
          name: "枪架速度(mm/s)",
          type: "line",
          data: i,
          markPoint: {data: [{type: "max", name: "最大值"}, {type: "min", name: "最小值"}]}
        }, {
          name: "送料速度(m/min)",
          type: "line",
          data: h,
          markPoint: {data: [{type: "max", name: "最大值"}, {type: "min", name: "最小值"}]}
        }]
      };
      chart.setOption(option)
    })
  }

  var e = new Date, n = "hour", i = "../static/data/" + n + "/" + get_time(e) + ".json";
  get_data(i, 1), $("#singleDateRange").DatePicker({startDate: moment()}), $("#submitit").click(function () {
    var a = $("#singleDateRange").val();
    n = "min";
    var e = "../static/data/" + n + "/" + a + ".json";
    get_data(e, 1)
  }), $("#changeit").click(function () {
    var a = $("#singleDateRange").val();
    n = "hour";
    var e = "../static/data/" + n + "/" + a + ".json";
    get_data(e, 1)
  })
});