interface Toast {
  id?: string;
  message: string;
  type: "success" | "warning";
  duration?: number;
}

interface Lecture {
  lectureName: string;
  lectureCode: string;
  lectureCredit: number;
  learned: boolean;
}
