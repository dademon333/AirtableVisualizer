export const comparePriority = (a: string, b: string) => {
  if (a.trim().toLowerCase() > b.trim().toLowerCase()) {
      return 1;
  } else {
      return -1;
  }
};