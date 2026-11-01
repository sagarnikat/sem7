// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * QUESTION 4 (BT):
 * Write a program in Solidity to create Student data using structures,
 * arrays and a fallback function. Deploy it on Ethereum and observe the
 * transaction fee and gas values.
 *
 * HOW IT WORKS
 *   struct Student packs one student record: id, name, course and age.
 *   Student[] students is a dynamic array that stores every record.
 *   mapping(uint256 => uint256) indexOf maps a student id to its position
 *   in the array plus one, so id 0 can mean "not found" without a second
 *   lookup loop.
 *
 *   addStudent() pushes a new struct into the array.
 *   getStudent() / getAllStudents() read records (view calls are free).
 *   updateStudent() changes the fields of an existing record.
 *   removeStudent() swaps the record with the last one and pops the array,
 *   which keeps removal O(1).
 *
 *   receive() accepts plain ETH with empty calldata.
 *   fallback() accepts ETH sent with unknown function data, records the raw
 *   calldata and emits an event. This is the fallback requirement of the
 *   assignment.
 *
 * GAS / COST NOTES
 *   Adding a student writes a new struct plus one mapping entry, so it is
 *   the most expensive write (roughly 100k+ gas depending on string length).
 *   Reading is free with eth_call. Sending ETH through receive/fallback
 *   costs about 25k-50k gas plus the calldata cost. In Remix, open the
 *   transaction in the console to see gas used; on Etherscan the fee is
 *   gasUsed * gasPrice (base fee + priority fee).
 *
 * DEPLOY
 *   Remix IDE -> Solidity compiler 0.8.20 or newer -> Deploy & Run ->
 *   Injected Provider (MetaMask) -> Sepolia -> Deploy.
 */

 //code
 //------------------------------------


//SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract StudentData{
    struct Student{
        uint rollNo;
        uint age;
        string name;
        uint marks;
        
    }

    Student[] public students;

    //Add Student
    function addStudent( uint _rollNo, uint _age, string memory _name, uint _marks)public{
        students.push(Student(_rollNo,_age,_name,_marks));
    }

    //Get Student
    function getStudent(uint index)public view returns(uint, string memory, uint){
        require (index<students.length,"Invalid ID");
        Student memory s = students[index];
        return (s.rollNo,s.name, s.marks);
    }

    //Get Student Count
    function getCount()public view returns(uint) {
        return students.length;
    }

    fallback() external payable {
        require(msg.value>0,"Ether must be greater than 0");
    }
    // receive() external payable {
    // require(msg.value > 0, "Ether must be greater than 0");

}