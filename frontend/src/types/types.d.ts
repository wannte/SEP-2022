interface Toast {
  id?: string;
  message: string;
  type: "success" | "warning";
  duration?: number;
}

interface Lecture {
  year: string;
  lecture_code: string;
  credit: number;
  required: boolean;
  lecture_name: string;
  semester: string;
  id: number;
  major: string;
  learned: boolean;
}
