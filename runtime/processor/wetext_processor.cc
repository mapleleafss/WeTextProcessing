// Copyright (c) 2022 Zhendong Peng (pzd17@tsinghua.org.cn)
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

#include "processor/wetext_processor.h"

using fst::StringTokenType;

namespace wetext {
Processor::Processor(const std::string& tagger_path,
                     const std::string& verbalizer_path) {
  tagger_.reset(StdVectorFst::Read(tagger_path));
  verbalizer_.reset(StdVectorFst::Read(verbalizer_path));
  compiler_ = std::make_shared<StringCompiler<StdArc>>(StringTokenType::BYTE);
  printer_ = std::make_shared<StringPrinter<StdArc>>(StringTokenType::BYTE);

  if (tagger_path.find("_tn_") != tagger_path.npos) {
    parse_type_ = ParseType::kTN;
  } else if (tagger_path.find("_itn_") != tagger_path.npos) {
    parse_type_ = ParseType::kITN;
  } else {
    LOG(FATAL) << "Invalid fst prefix, prefix should contain"
               << " either \"_tn_\" or \"_itn_\".";
  }
}

std::string Processor::ShortestPath(const StdVectorFst& lattice) {
  StdVectorFst shortest_path;
  fst::ShortestPath(lattice, &shortest_path, 1, true);

  std::string output;
  printer_->operator()(shortest_path, &output);
  return output;
}

std::string Processor::Compose(const std::string& input,
                               const StdVectorFst* fst) {
  StdVectorFst input_fst;
  compiler_->operator()(input, &input_fst);

  StdVectorFst lattice;
  fst::Compose(input_fst, *fst, &lattice);
  return ShortestPath(lattice);
}

std::string Processor::Tag(const std::string& input) {
  if (input.empty()) {
    return "";
  }
  return Compose(input, tagger_.get());
}

std::string Processor::Verbalize(const std::string& input) {
  if (input.empty()) {
    return "";
  }
  TokenParser parser(parse_type_);
  std::string output = parser.Reorder(input);

  output = Compose(output, verbalizer_.get());
  output.erase(std::remove(output.begin(), output.end(), '\0'), output.end());
  return RemoveSpace(output);
}

std::string Processor::Normalize(const std::string& input) {
  return Verbalize(Tag(input));
}

std::string Processor::RemoveSpace(const std::string& input) {
  if (input.empty()) {
    return "";
  }
  std::string output = "";
  int size = input.size();
  char percent = '%', last_valid_ch = ' ', aftch = ' ';
  bool before_num_flag, after_num_flag;
  bool before_char_flag, after_char_flag;
  bool before_percent_flag, after_percent_flag;

  for (int i=0; i<size; ++i) {
    char ch = input[i];
    if (ch != ' ') {
      output += ch;
      last_valid_ch = ch;
    }
    else {
      if ( (i == size - 1) || (input[i+1] == ' ') ) {
        continue;
      }
      aftch = input[i+1];
      before_num_flag = (last_valid_ch >= '0' && last_valid_ch <= '9');
      before_char_flag = false;
      before_percent_flag = false;
      after_percent_flag = false;

      if (!before_num_flag) {
        before_char_flag = ((last_valid_ch >= 'a' && last_valid_ch <= 'z') || \
                           (last_valid_ch >= 'A' && last_valid_ch <= 'Z') || \
                           last_valid_ch == ',' || last_valid_ch == '.' );
        if (!before_char_flag) {
          before_percent_flag = (last_valid_ch == percent);
        }
      }
      after_num_flag = (aftch >= '0' && aftch <= '9');
      after_char_flag = false;
      if (!after_num_flag) {
        after_char_flag = ((aftch >= 'a' && aftch <= 'z') || \
                           (aftch >= 'A' && aftch <= 'Z') || \
                           aftch == ',' || aftch == '.');
        after_percent_flag = ( aftch == percent);
      }

      if ( before_char_flag || after_char_flag || \
           (before_num_flag && after_num_flag) || \
           ((before_char_flag || before_num_flag) && after_percent_flag) || \
           (before_percent_flag && (after_char_flag || after_num_flag)) ) {
        output += " ";
      }
    }
  }
  return output;
}


}  // namespace wetext
