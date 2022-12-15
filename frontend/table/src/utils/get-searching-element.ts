type Props = {
  query: string;
  initData: {
    name: string;
    to: string;
  }[];
}

export const getSearchingElement = ({initData, query}: Props) => {
  return initData.filter(item => {
      if (query === "") {
          return item;
      } else if (item.name.toLowerCase().trim().includes(query.toLowerCase().trim())) {
          return item;
      } else return null;
  });
};
