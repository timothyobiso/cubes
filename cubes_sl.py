import streamlit as st
import itertools

def rotate_cube(cube):
    rotations = []
    index, cube_config = cube
    for i in range(3):
        front = cube_config[i]
        others = cube_config[:i] + cube_config[i+1:]
        for j in range(2):
            rotations.append((index, [front] + others[j:] + others[:j]))
            rotations.append((index, [front] + [others[j][::-1]] + [others[1-j][::-1]]))
    return rotations

def valid_configuration(permutation, requirements):
    for orientations in itertools.product(*[rotate_cube(cube) for cube in permutation]):
        if all(set(orientation[1][0]) == set(req) for orientation, req in zip(orientations, requirements)):
            return orientations
    return False

def find_solutions(cubes, requirements):
    solutions = []
    for perm in itertools.permutations(cubes):
        valid_orient = valid_configuration(perm, requirements)
        if valid_orient:
            solutions.append(valid_orient)
    return solutions

def main():
    st.title("Cube Color Opposite Solver")
    num_cubes = st.number_input("Enter the number of cubes", min_value=1, value=3)
    cubes = []
    requirements = []
    
    for i in range(num_cubes):
        with st.expander(f"Cube {i+1} Configuration"):
            cube = [st.text_input(f"Pair 1 for Cube {i+1} (color1 color2)", key=f"cube{i+1}pair1").split(),
                    st.text_input(f"Pair 2 for Cube {i+1} (color3 color4)", key=f"cube{i+1}pair2").split(),
                    st.text_input(f"Pair 3 for Cube {i+1} (color5 color6)", key=f"cube{i+1}pair3").split()]
            cubes.append((i+1, cube))
    
    with st.expander("Requirements"):
        for i in range(num_cubes):
            req = st.text_input(f"Required opposite pair for position {i+1} (color1 color2)", key=f"req{i+1}").split()
            requirements.append(req)
    
    if st.button("Solve"):
        if any(not cube[1][0] for cube in cubes):  # Check if any cube configuration is incomplete
            st.error("Please complete all cube configurations.")
        elif any(len(req) != 2 for req in requirements):
            st.error("Please complete all requirements properly.")
        else:
            solutions = find_solutions(cubes, requirements)
            if solutions:
                st.success("Valid configurations found:")
                for idx, solution in enumerate(solutions, 1):
                    st.subheader(f"Configuration {idx}:")
                    for i, (index, cube) in enumerate(solution):
                        st.write(f"Cube {index} (originally input as cube {index}): {cube}")
            else:
                st.error("No valid configuration found.")

if __name__ == "__main__":
    main()

