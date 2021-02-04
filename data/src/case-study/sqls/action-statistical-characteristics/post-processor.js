module.exports = async function(data) {
  let ret = '| # | repo_name | resolve_period_avg | respond_period_avg | resolve_period_median | respond_period_median | count |\n';
  ret += '|:--:|:--:|:--:|:--:|:--:|:--:|:--:|\n';
  data.forEach((item, index) => {
    ret += `| ${index + 1} | ${item.repo_name} | ${item.resolve_period_avg} | ${item.respond_period_avg} | ${item.resolve_period_median} | ${item.respond_period_median} | ${item.count} |\n`;
  });
  return ret;
}
