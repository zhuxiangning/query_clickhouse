module.exports = async function(data, config) {
  if (!Array.isArray(data)) {
    throw new Error('Invalid data');
  }
  var min = Number.MAX_VALUE;
  var max = Number.MIN_VALUE;
  data.forEach(i => {
    i.count = parseInt(i.count);
    if (i.count > max) max = i.count;
    if (i.count < min) min = i.count;
  });

  var d = [];
  for (var i = 0; i < 24; i++) {
    var row = data.find(item => (item.hour == i));
    if (row) {
      // prevent zero for min
      var week_count = 0;
      for (var j = row.length - 1; j >= 0; j--) {
        week_count += row[j].count;
      }
      var c = Math.ceil((week_count - min*7) * 10 / ((max - min)*7));
      d.push(Math.max(1, c));
    } else {
      d.push(0);
    }
  }
  var k = 12;
  var d2 = d.concat(d);
  var cur_max_conti_index = 0;
  var max_conti_k_hours = d2[cur_max_conti_index];
  for(var i = 0; i < d.length; i++) {
    var temp_sum = 0;
    for(var m = i; m < i + k; m++) {
      temp_sum += d2[m]
    }
    if(max_conti_k_hours < temp_sum){
      max_conti_k_hours = temp_sum
      cur_max_conti_index = i
    }
  }
  var GMT_time_zone;
  if(cur_max_conti_index < 12) {
    GMT_time_zone = cur_max_conti_index;
  }
  else{
    GMT_time_zone = cur_max_conti_index - 24;
  }
  return `${config.baseUrl}svgrenderer/github/${config.owner}/${config.repo}?path=sqls/developers-timezone-predict/image.svg&data=${JSON.stringify(d)}&GMT_time_zone=${JSON.stringify(GMT_time_zone)}&max_conti_k_hours=${JSON.stringify(max_conti_k_hours)}`;
}
