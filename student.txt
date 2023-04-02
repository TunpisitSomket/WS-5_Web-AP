// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

contract Studentlist {
    struct Student {
        uint256 id;
        string f_lname;
        uint256 gpax;
        bool flag;
    }

    mapping(uint256 => Student) private students;
    uint256[] private studentIds;

    //เพิ่มนักเรียน
    function addStudent(uint256 _id, string memory _name, uint256 _gpax) public {
        require(!students[_id].flag, "Student with this ID already exists.");
        students[_id] = Student(_id, _name, _gpax, true);
        studentIds.push(_id);
    }

    //อัปเดตนักเรียน
    function updateStudent(uint256 _id, string memory _name, uint256 _gpax) public {
        require(students[_id].flag, "Student with this ID does not exist.");
        students[_id].f_lname = _name;
        students[_id].gpax = _gpax;
    }

    //ลบนักเรียน
    function deleteStudent(uint256 _id) public {
        require(students[_id].flag, "Student with this ID does not exist.");
        students[_id].flag = false;
    }

    //หานักเรียนตามid
    function getStudentById(uint256 _id) public view returns (Student memory) {
        require(students[_id].flag, "Student with this ID does not exist.");
        return students[_id];
    }

    //นักเรียนทั้งหมด
    function getAllStudents() public view returns (Student[] memory) {
        uint256 active_students = 0;
        for (uint256 i = 0; i < studentIds.length; i++) {
            if (students[studentIds[i]].flag) {
                active_students++;
            }
        }

        Student[] memory all_of_students = new Student[](active_students);
        uint256 index = 0;
        for (uint256 i = 0; i < studentIds.length; i++) {
            if (students[studentIds[i]].flag) {
                all_of_students[index] = students[studentIds[i]];
                index++;
            }
        }

        return all_of_students;
    }
}


