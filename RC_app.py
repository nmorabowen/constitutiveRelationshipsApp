import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import math
import re

from baseUnits import mm, cm, m, inches, ft, N, kN, kgf, tf, lbf, kip, MPa, kPa, Pa, ksi 
from plotApeConfig import set_default_plot_params, blueAPE
set_default_plot_params()

import ConstitutiveRelationships as cr

def display_header():
    st.header("Uniaxial Constitutive Relationships")
    
    text = """
    Uniaxial constitutive relationships for unconfined concrete, confined concrete, and steel.
    
    Concrete: *Mandel models*
    
    Steel: *Bi Linear Model with Strain Hardening*
    
    """
    st.markdown(text)

def display_pip_install():
    st.code(
        """
        # Install python packages
        # Not editable
        pip install https://github.com/nmorabowen/APE_Public/raw/main/dist/APE_Public-0.1-py3-none-any.whl
        # Editable
        pip install -e git+https://github.com/nmorabowen/APE_Public.git#egg=APE_Public
        """, language='python', line_numbers=True
    )

def display_dependencies_code():
    st.code(f"""
        # ========================================
        # Import Dependencies
        # ========================================
        
        import ConstitutiveRelationships as cr
        """, language='python', line_numbers=True)

def create_top_buttons():
    plot_current, plot_all, erase_all, load_typical = st.columns(4)
    
    with plot_all:
        if st.button('Plot All'):
            st.session_state.plot_all_trigger = True
    
    with plot_current:
        if st.button('Plot Current'):
            st.session_state.plot_current_trigger = True
            #st.success('Plotted')
    
    with erase_all:
        if st.button('Erase All Plots'):
            st.session_state.matObjects = []  # Clear all plots
            st.rerun()
            #st.success('All plots erased!')
            
    with load_typical:
        if st.button('Load Typical'):
            default_materials()
            st.rerun()
            #st.success('Materials Loaded')

def generate_material_list():
    # Function create a list of material objects
    return [str(material.name) for material in st.session_state.matObjects]

def create_stored_material_select_box():
    st.sidebar.header("Stored Plots")
    material_list = generate_material_list()
    selected_material = st.sidebar.selectbox("Selected Material", material_list)
    st.session_state.selected_material_name = selected_material
    return selected_material

def parse_expresion(input_string):
    # Function to eeror handle the unit definition and evaluate the final expresion
    units={
        'mm':mm,
        'cm':cm,
        'm':m,
        'inches':inches,
        'in':inches,
        'ft':ft,
        'N':N,
        'kN':kN,
        'kgf':kgf,
        'tf':tf,
        'lbf':lbf,
        'kip':kip,
        'MPa':MPa,
        'kPa':kPa,
        'Pa':Pa,
        'ksi':ksi
    }
    # Replace the units in the input string
    for unit, value in units.items():
        input_string=input_string.replace(unit,f'{value}')
    # Evaluate the expresion
    try:
        result = eval(re.sub(r'[^0-9+\-*/.()]', '', input_string))
        return result
    except Exception as e:
        st.error(f"Evaluation Error: {e}")
        return None

def createBilinealSteel():
    
    name = st.sidebar.text_input('name: ', value='name')
    fy_input = st.sidebar.text_input("fy", value=420.0)
    fsu_input = st.sidebar.text_input("fsu", value=630.0)
    esh_input = st.sidebar.text_input("esh", value=0.0080)
    esu_input = st.sidebar.text_input("esu", value=0.12)
    Es_input = st.sidebar.text_input("Es", value=200000.0)
    Esh_input = st.sidebar.text_input("Esh", value=7000.0)
    color = st.sidebar.color_picker('color', value='#000000')
    
    # Evaluate the internal expressions
    fy=parse_expresion(fy_input)
    fsu=parse_expresion(fsu_input)
    esh=parse_expresion(esh_input)
    esu=parse_expresion(esu_input)
    Es=parse_expresion(Es_input)
    Esh=parse_expresion(Esh_input)
    
    mat_object = cr.uniaxialBilinealSteel(
        name=name,
        fy=fy,
        fsu=fsu,
        esh=esh,
        esu=esu,
        Es=Es,
        Esh=Esh,
        color=color
    )
    return mat_object
    
def createUnconfinedConcrete():
    name=st.sidebar.text_input('name',value='name')
    fco_input=st.sidebar.text_input('fco', value=24)
    eco_input=st.sidebar.text_input('eco', value=0.002)
    ec_sprall_input=st.sidebar.text_input('ec_sprall', value=0.006)
    color = st.sidebar.color_picker('color', value='#000000')
    
    fco=parse_expresion(fco_input)
    eco=parse_expresion(eco_input)
    ec_sprall=parse_expresion(ec_sprall_input)
    
    mat_object = cr.uniaxialUnconfinedConcrete(
        name=name,
        fco=fco,
        eco=eco,
        ec_sprall=ec_sprall,
        color=color
    )
    return mat_object

def createConfinedConcrete():
    name=st.sidebar.text_input('name', value='name')
    fco_input=st.sidebar.text_input('fco', value=24)
    eco_input=st.sidebar.text_input('eco', value=0.003)
    b_input=st.sidebar.text_input('b', value=300)
    h_input=st.sidebar.text_input('h', value=400)
    rec_input=st.sidebar.text_input('rec', value=30)
    num_var_b_input=st.sidebar.text_input('num_var_b', value=3)
    num_var_h_input=st.sidebar.text_input('num_var_h', value=4)
    phi_longitudinal_input=st.sidebar.text_input('phi_longitudinal', value=16)
    num_est_perpendicular_b_input=st.sidebar.text_input('num_est_perpendicular_b', value=2)
    num_est_perpendicular_h_input=st.sidebar.text_input('num_est_perpendicular_h', value=2)
    phi_estribo_input=st.sidebar.text_input('phi_estribo', value=10)
    s_input=st.sidebar.text_input('s', value=100)
    fye_input=st.sidebar.text_input('fye', value=420)
    esu_estribo_input=st.sidebar.text_input('esu_estribo', value=0.09)
    color = st.sidebar.color_picker('color', value='#000000')
    
    fco=parse_expresion(fco_input)
    eco=parse_expresion(eco_input)
    b=parse_expresion(b_input)
    h=parse_expresion(h_input)
    rec=parse_expresion(rec_input)
    num_var_b=parse_expresion(num_var_b_input)
    num_var_h=parse_expresion(num_var_h_input)
    phi_longitudinal=parse_expresion(phi_longitudinal_input)
    num_est_perpendicular_b=parse_expresion(num_est_perpendicular_b_input)
    num_est_perpendicular_h=parse_expresion(num_est_perpendicular_h_input)
    phi_estribo=parse_expresion(phi_estribo_input)
    s=parse_expresion(s_input)
    fye=parse_expresion(fye_input)
    esu_estribo=parse_expresion(esu_estribo_input)
    
    mat_object=cr.uniaxialConfinedConcrete(
        name=name,
        fco=fco,
        eco=eco,
        b=b,
        h=h,
        rec=rec,
        num_var_b=num_var_b,
        num_var_h=num_var_h,
        phi_longitudinal=phi_longitudinal,
        num_est_perpendicular_b=num_est_perpendicular_b,
        num_est_perpendicular_h=num_est_perpendicular_h,
        phi_estribo=phi_estribo,
        s=s,
        fye=fye,
        esu_estribo=esu_estribo,
        color=color
    )
    return mat_object

def create_material_select_box(material_type):
    
    if material_type == "BiLineal Steel":
        mat_object=createBilinealSteel()
        mat_object_code_string=code_block_steel(mat_object)
        return mat_object, mat_object_code_string
    
    if material_type == "Uncofined Mandel Concrete":
        mat_object=createUnconfinedConcrete()
        mat_object_code_string=code_block_uc_string(mat_object)
        return mat_object, mat_object_code_string
    
    if material_type == "Confined Mandel Steel":
        mat_object=createConfinedConcrete()
        mat_object_code_string=code_block_cc_string(mat_object)
        return mat_object, mat_object_code_string

def code_block_steel(mat_object):
    mat_object_code_string=f"""
        # python syntax
        cr.uniaxialBilinealSteel(
            name={mat_object.name}, 
            fy={mat_object.fy}, 
            fsu={mat_object.fsu}, 
            esh={mat_object.esh}, 
            esu={mat_object.esu}, 
            Es={mat_object.Es}, 
            Esh={mat_object.Esh}, 
            plot=False, 
            delta=15, 
            color='k', 
            marker=None
        )
        """
    return mat_object_code_string

def code_block_uc_string(mat_object):
    mat_object_code_string=f"""
    # python syntax
    cr.uniaxialUnconfinedConcrete(
        name={mat_object.name},
        fco={mat_object.fco},
        eco={mat_object.eco},
        ec_sprall={mat_object.ec_sprall},
        color={mat_object.color}
    )
    """
    return mat_object_code_string

def code_block_cc_string(mat_object):
    mat_object_code_string = f"""
    # python syntax
    cr.uniaxialConfinedConcrete(
        name={mat_object.name},
        fco={mat_object.fco},
        eco={mat_object.eco},
        b={mat_object.b},
        h={mat_object.h},
        rec={mat_object.rec},
        num_var_b={mat_object.num_var_b},
        num_var_h={mat_object.num_var_h},
        phi_longitudinal={mat_object.phi_longitudinal},
        num_est_perpendicular_b={mat_object.num_est_perpendicular_b},
        num_est_perpendicular_h={mat_object.num_est_perpendicular_h},
        phi_estribo={mat_object.phi_estribo},
        s={mat_object.s},
        fye={mat_object.fye},
        esu_estribo={mat_object.esu_estribo},
        color={mat_object.color}
    )
    """
    return mat_object_code_string

def print_code_block(mat_object_code_string):
    st.code(f'{mat_object_code_string}', language='python', line_numbers=True)
    
def plot_current(mat_object):
    fig, ax = plt.subplots(figsize=(10, 5))
    mat_object.plot(ax=ax)
    st.pyplot(fig)
    st.success('The required input parameters for Xtract are:')

def plot_all(material_selection):
    fig, ax = plt.subplots(figsize=(10, 5))
    #for material in st.session_state.matObjects:
    for material in material_selection:
        material.plot(ax=ax)
    st.pyplot(fig)

def default_materials():
    A36=cr.uniaxialBilinealSteel('A36', 36*ksi, 1.50*36*ksi)
    A572=cr.uniaxialBilinealSteel('A572', 50*ksi, 1.10*50*ksi)
    A706Gr60=cr.uniaxialBilinealSteel('A706Gr60', 60*ksi, 1.25*60*ksi)
    
    fc240uc=cr.uniaxialUnconfinedConcrete('fc240uc', 240*kgf/cm**2)

    fc240cc=cr.uniaxialConfinedConcrete('fc240cc', 24, 0.003, 300, 400, 30, 3, 4, 16, 2, 2, 10, 200, 420, 0.09)
    
    st.session_state.matObjects=[A36, A572, A706Gr60, fc240uc, fc240cc]
    st.session_state.matObjectsCodeString=[code_block_steel(A36), code_block_steel(A572), code_block_steel(A706Gr60), code_block_uc_string(fc240uc), code_block_cc_string(fc240cc)]

def display_footer():
    footer = """
    <style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: white;
        color: black;
        text-align: center;
        padding: 10px;
        border-top: 1px solid #eaeaea;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .footer .logo {
        height: 60px; /* Increased size */
        margin-right: 20px;
    }
    .footer .separator {
        border-left: 2px solid #eaeaea;
        height: 120px;
        margin-right: 20px;
    }
    </style>
    <div class="footer">
        <img class="logo" src="https://raw.githubusercontent.com/nmorabowen/constitutiveRelationshipsApp/main/APE_LOGO.png" alt="APE Logo">
        <div class="separator"></div>
        <div>
            <p>Developed by Nicolás Mora Bowen | <a href="https://www.ape-ec.com" target="_blank">APE</a> | <a href="https://www.nmorabowen.com" target="_blank">Nicolás Mora Bowen</a> | <a href="https://github.com/nmorabowen" target="_blank">GitHub</a></p>
            <p>© Version 1.0.1  - July, 2024</p>
        </div>
    </div>
    """
    st.markdown(footer, unsafe_allow_html=True)


def main():
    if "matObjects" not in st.session_state:
        st.session_state.matObjects = []
        st.session_state.matObjectsCodeString = []

    if "plot_all_trigger" not in st.session_state:
        st.session_state.plot_all_trigger = False

    if "plot_current_trigger" not in st.session_state:
        st.session_state.plot_current_trigger = False
        
    if "previous_material_selection" not in st.session_state:
        st.session_state.previous_material_selection=None

    material_selection=st.multiselect(label='Select the curves you want to plot',options=st.session_state.matObjects)
    
    display_header()
    
    st.divider()
    with st.expander("VIEW PYTHON IMPLEMENTATION:"):
        display_pip_install()
        display_dependencies_code()
    
    st.divider()
    create_top_buttons()
    
    st.divider()
    create_stored_material_select_box()

    st.sidebar.header("Input Material Properties")
    material_type = st.sidebar.selectbox("Select Material Type", ["Confined Mandel Steel", "Uncofined Mandel Concrete", "BiLineal Steel"])

    mat_object, mat_object_code_string = create_material_select_box(material_type)
    
    if st.sidebar.button("Save"):
        st.session_state.matObjects.append(mat_object)
        st.session_state.matObjectsCodeString.append(mat_object_code_string)
        create_stored_material_select_box()
        st.rerun()

    if st.session_state.plot_current_trigger:
        selected_material = None
        selected_mat_code_string=None
        if st.session_state.selected_material_name:
            for idx, mat in enumerate(st.session_state.matObjects):
                if mat.name == st.session_state.selected_material_name:
                    selected_material = mat
                    selected_mat_code_string=st.session_state.matObjectsCodeString[idx]
                    break

            if selected_material:
                print_code_block(selected_mat_code_string)
                plot_current(selected_material)
            else:
                st.warning("Selected material not found.")
        else:
            st.warning("No material selected.")
        st.session_state.plot_current_trigger = False

    if st.session_state.plot_all_trigger:
        plot_all(material_selection)
        st.session_state.plot_all_trigger = False

        
    display_footer()

if __name__ == "__main__":
    main()
