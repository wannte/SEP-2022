export const majors = {
  BS: "생명",
  CH: "화학",
  EC: "전기전자컴퓨터공학",
  EV: "지구환경공학",
  GS: "기초교육학부",
  MA: "신소재공학",
  MC: "기계공학",
  PS: "물리",
  ALL: "전체",
};

export type Major = keyof typeof majors;
