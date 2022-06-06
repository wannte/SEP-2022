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

interface Lectures {
  lectures: Array<Lecture>;
  credit: number;
}

interface Basic {
  freshman_semina: Lectures;
  liberal_arts: Lectures;
  required_language: Lectures;
  required_science: Lectures;
}

interface FreeSelect {
  basic: Lectures;
  language_sw: Lectures;
  liberal_arts: Lectures;
  other: Lectures;
  other_major: Lectures;
  other_pre_required: Lectures;
  pre_required: Lectures;
}

interface Major {
  non_required: Lectures;
  required: Lectures;
}

interface NonCredit {
  art_music: Lectures;
  coloquium: Lectures;
  sport: Lectures;
}

interface Research {
  research: Lectures;
}

interface Result {
  basic: Basic;
  free_select: FreeSelect;
  major: Major;
  non_credit: NonCredit;
  research: Research;
}
