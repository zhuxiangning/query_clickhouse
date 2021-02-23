module.exports = async function(data) {
  let ret = '| # | use_language | count | top_actor | activity | part_repo_count | \n';
  ret += '|:--:|:--:|:--:|:--:|:--:|:--:| \n';
  data.forEach((item, index) => {
    ret += `| ${index + 1} | ${item.use_language} | ${item.count} | ${item.top_actor} | ${item.activity} | ${item.part_repo_count} |\n`;
  });
  return ret;
}
